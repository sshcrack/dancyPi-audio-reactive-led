from led.gradient import calculateGradient
import led.tools as tools
import time
import numpy as np
from distutils.command.config import config
from httpserver.currVars import getFilterMode, getGeneralSpeed, getGradient

_time_prev = time.time()
rgb_index = 0
def applyFilters(data):
    global _time_prev, rgb_index
    currTime = time.time() * 1000

    filter_mode = getFilterMode()
    speed = getGeneralSpeed()
    gradient = getGradient()

    r, g, b = data
    gradient_pixels = calculateGradient(len(r), gradient)

    for i in range(len(r)):
        maxVal = np.amax(np.array([r[i], g[i], b[i]]))
        if filter_mode == "hex":
            desired_rgb = np.array(gradient_pixels[i])

            r[i] = maxVal * desired_rgb[0]
            g[i] = maxVal * desired_rgb[1]
            b[i] = maxVal * desired_rgb[2]

        if filter_mode == "rainbow":
            rgb_index += (currTime - _time_prev) * .0005 * speed
            local_led_index = int(rgb_index + i)
            values = np.array(tools.wheel(local_led_index)) / 255

            if rgb_index >= 255:
                rgb_index = 0

            r[i] = values[0] * maxVal
            g[i] = values[1] * maxVal
            b[i] = values[2] * maxVal

    _time_prev = currTime
    return np.array([r, g, b])
