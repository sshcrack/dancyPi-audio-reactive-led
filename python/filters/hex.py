from httpserver.currVars import getGradient
import numpy as np
from tools.gradient import calculateGradient


def hex(data):
    r, g, b = data

    gradient = getGradient()

    gradient_pixels = calculateGradient(len(r), gradient)

    for i in range(len(r)):
        maxVal = np.amax(np.array([r[i], g[i], b[i]]))
        d_r, d_g, d_b = np.array(gradient_pixels[i])

        r[i] = maxVal * d_r
        g[i] = maxVal * d_g
        b[i] = maxVal * d_b

    return np.array([ r, g, b])
