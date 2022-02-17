from math import floor
import numpy as np
from httpserver.currVars import getConfig, getGeneralSpeed
import config
from tools.tools import getDeltaTime

max_pixels = config.N_PIXELS
center_pos = max_pixels / 2
print("Initial", center_pos)
# 1 = 0 to 255
# -1 = 255 to 0
direction = True

def scanner():
    global center_pos, direction, max_pixels

    delta = getDeltaTime()
    speed = getGeneralSpeed()

    full_bright = getConfig("scanner_size")
    shadow_size = getConfig("scanner_shadow")
    
    # 2 times for both sides
    total_size = full_bright + 2 * shadow_size
    half_size = total_size / 2


    if center_pos <= half_size:
        direction = 1
    elif center_pos >= max_pixels - half_size:
        direction = -1

    center_pos += delta * speed * 150 * direction
    channel = []

    min_shadow = center_pos - shadow_size
    max_shadow = center_pos + shadow_size
    for i in range(max_pixels):
        if not ( i >= min_shadow and i <= max_shadow):
            channel.append(0)
            continue

        # could also be min_shadow
        distance = 1 - abs((i - center_pos) / shadow_size)
        brightness = floor(min(distance * 255, 255))

        channel.append(brightness)

    return np.array([ channel, channel, channel ])
