import math
import numpy as np
from typing import List
#
#def gaussian(x, a, b, c, d=0):
#    return a * math.exp(-(x - b)**2 / (2 * c**2)) + d
#
#def pixel(x, width=100, map=[], spread=1.5):
#    width = float(width)
#    r = sum([gaussian(x, p[1][0], p[0] * width, width/(spread*len(map))) for p in map])
#    g = sum([gaussian(x, p[1][1], p[0] * width, width/(spread*len(map))) for p in map])
#    b = sum([gaussian(x, p[1][2], p[0] * width, width/(spread*len(map))) for p in map])
#    return min(1.0, r), min(1.0, g), min(1.0, b)
#
#def colorToPercent(heatmap: List[List]):
#    out = []
#    for i in range(len(heatmap)):
#        el = heatmap[i]
#        data = el[0]
#        rgb = np.array(el[1]) / 255
#
#        out.append([ data, rgb ])
#    return out
#
# Heatmap with max 255
#def calculateGradient(width: int, heatmap: List[List]):
#    pixels = []
#    heatmap = colorToPercent(heatmap)
#    for i in range(width):
#        pixels.append(pixel(i, width, heatmap))
#
#    return np.array(pixels)


def lerp(a, b, t):
    return a*(1 - t) + b*t
    
def calculateGradient(width: int, grad: List[List]):
    detail = 1 / width
    out = []
    for i in range(width):
        closestMinStep, closestMinRGB = -100, None
        closestMaxStep, closestMaxRGB = 100,  None
        curr = detail * i
        for [step, rgb] in grad:
            if closestMinStep < step and step <= curr:
                closestMinStep = step
                closestMinRGB = np.array(rgb)

            if closestMaxStep > step and step > curr:
                closestMaxStep = step
                closestMaxRGB = np.array(rgb)


        relativeStep = (curr - closestMinStep) / (closestMaxStep - closestMinStep)
        out.append(lerp(closestMinRGB, closestMaxRGB, relativeStep) / 255)

    return out