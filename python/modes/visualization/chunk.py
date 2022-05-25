import math

import config
from httpserver.currVars import getConfig
from modes.visualization.visualization import interpolate, common_mode, r_filt, b_filt
import numpy as np

_prev_spectrum = np.tile(0.01, config.N_PIXELS // 2)


def chunk(mel):
    """Effect that maps the Mel filterbank frequencies onto the LED strip"""
    global _prev_spectrum
    mel = np.copy(interpolate(mel, config.N_PIXELS // 2))
    common_mode.update(mel)
    diff = mel - _prev_spectrum
    _prev_spectrum = np.copy(mel)
    # Color channel mappings
    r = r_filt.update(mel - common_mode.value)
    g = np.abs(diff)
    b = b_filt.update(np.copy(mel))
    # Mirror the color channels for symmetric output
    r = np.concatenate((r[::-1], r))
    g = np.concatenate((g[::-1], g))
    b = np.concatenate((b[::-1], b))

    chunks = getConfig("chunk_chunks")
    singleChunk = len(r) / chunks
    output = np.tile(1, (3, config.N_PIXELS))
    for i in range(chunks):
        startChunk = math.floor(singleChunk * i)
        endChunk = math.floor(singleChunk * (i + 1))

        rChunk = np.average(r[startChunk:endChunk]) * 255
        gChunk = np.average(g[startChunk:endChunk]) * 255
        bChunk = np.average(b[startChunk:endChunk]) * 255
        output[0][startChunk:endChunk] = rChunk
        output[1][startChunk:endChunk] = gChunk
        output[2][startChunk:endChunk] = bChunk

    return output
