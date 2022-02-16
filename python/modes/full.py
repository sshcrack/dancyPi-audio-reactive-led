import numpy as np
import config

def full():
    justWhite = [ ]
    for _ in range(config.N_PIXELS):
        justWhite.append([ 255 ])

    return np.array([ justWhite, justWhite, justWhite ])
