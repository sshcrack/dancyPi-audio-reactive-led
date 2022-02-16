from httpserver.currVars import getGeneralSpeed
import numpy as np
import tools.tools as tools

rgb_index = 0
def rainbow(data):
    global _time_prev, rgb_index

    r, g, b = data
    speed = getGeneralSpeed()
    deltaTime = tools.getDeltaTime()


    for i in range(len(r)):
        maxVal = np.amax(np.array([r[i], g[i], b[i]]))
        rgb_index += deltaTime * speed
        local_led_index = int(rgb_index + i)
        values = np.array(tools.wheel(local_led_index)) / 255

        if rgb_index >= 255:
            rgb_index = 0

        r[i] = values[0] * maxVal
        g[i] = values[1] * maxVal
        b[i] = values[2] * maxVal

    return np.array([ r, g, b])