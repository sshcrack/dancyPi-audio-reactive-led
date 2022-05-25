from typing import List
from httpserver.currVars import getConfig, getGeneralSpeed
import numpy as np
import tools.tools as tools

rgb_index = 0


def rainbow(data):
    global rgb_index

    r, g, b = data
    speed = getConfig("rainbow_speed")
    if speed is None:
        speed = getGeneralSpeed()

    deltaTime = tools.getDeltaTime()

    for i in range(len(r)):
        maxVal = getMax([r[i], g[i], b[i]])
        rgb_index += deltaTime * speed
        local_led_index = int(rgb_index + i)
        values = np.array(tools.wheel(local_led_index)) / 255

        if rgb_index >= 255:
            rgb_index = 0

        r[i] = values[0] * maxVal
        g[i] = values[1] * maxVal
        b[i] = values[2] * maxVal

    return np.array([r, g, b])


def getMax(arr):
    maxVal = arr[0]
    for x in arr:
        if x > maxVal:
            maxVal = x

    return maxVal
