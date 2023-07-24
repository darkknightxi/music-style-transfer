import numpy as np
import os
import pypianoroll as pr

num_timestamps = 1000
num_pitches = 128

def load(style):
    X = None
    Y = None
    data_folder = f'data/{style}'
    for filename in os.listdir(data_folder):
        try:
            filepath = os.path.join(data_folder, filename)
            (matrix_x, matrix_y) = parse_multiple_dynamic(filepath)
            matrix_x = np.concatenate(matrix_x, axis=0)
            matrix_y = np.concatenate(matrix_y, axis=0)
            if X is None:
                X = matrix_x
            else:
                X = np.concatenate((X, matrix_x), axis=0)
            if Y is None:
                Y = matrix_y
            else:
                Y = np.concatenate((Y, matrix_y), axis=0)
        except Exception as e:
            pass
    print(f'X shape: {X.shape}')
    print(f'Y shape: {Y.shape}')
    return (X,Y)

def parse_multiple_dynamic(file):
    pianoroll = pr.read(file).tracks[0].pianoroll
    shape = pianoroll.shape
    print(shape)
    
    matrix_x = []
    matrix_y = []
    
    total_timestamps = shape[0]
    t = 0
    while t+1000 <= total_timestamps:
        matrix_tx = ((pianoroll[t:t+1000, :] > 0)*1).reshape(1, num_timestamps, num_pitches)
        matrix_ty = pianoroll[t:t+1000, :].reshape(1, num_timestamps, num_pitches)
        matrix_x.append(matrix_tx)
        matrix_y.append(matrix_ty)
        t += 1000
    print(f"done parsing {file} dynamically into {len(matrix_x)} segments of 1000 timestamps")
    return (matrix_x, matrix_y)

def save(matrix, filename):
    track = pr.Track(pianoroll=matrix, program=0, is_drum=False, name='classic music transferred from jazz')
    multitrack = pr.Multitrack(tracks=[track])
    pr.utilities.write(multitrack, filename)
    print("{} saved".format(filename))
    