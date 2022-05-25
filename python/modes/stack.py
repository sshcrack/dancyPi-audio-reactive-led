from math import ceil, floor

import config
import numpy as np
from httpserver.currVars import getConfig, getGeneralSpeed
from tools.tools import getDeltaTime

curr_stack = 0
pixel_locations = []
animating_out = False
animating_status = 0


def stack():
    global curr_stack, pixel_locations, animating_out, animating_status
    general_speed_modifier = .25

    delta = getDeltaTime()
    speed = getGeneralSpeed()

    max_pixels = config.N_PIXELS
    concurrent = getConfig("stack_concurrent")
    stack_speed = getConfig("stack_speed")

    if curr_stack >= max_pixels:
        curr_stack = 0
        pixel_locations = []
        animating_out = True

    if animating_out:
        channel = []
        pixels = floor((1 - animating_status) * max_pixels)
        animating_status += delta * speed * general_speed_modifier

        if animating_status > 1:
            animating_out = False
            animating_status = 0
        else:
            for i in range(max_pixels):
                if pixels >= i:
                    channel.append(255)
                    continue
                channel.append(0)

            return np.array([channel, channel, channel])

    pixel_length = len(pixel_locations)
    if pixel_length != concurrent:
        diff = concurrent - pixel_length
        if diff != 0:
            single_size = 1 / concurrent
            for i in range(diff):
                pixel_locations.append(max_pixels + single_size * i * max_pixels)

    for i in range(len(pixel_locations)):
        curr = pixel_locations[i]
        curr -= delta * speed * general_speed_modifier * stack_speed * max_pixels
        if curr >= 0:
            pixel_locations[i] = curr
        else:
            pixel_locations[i] = 0

    val = []

    def getMovePixel(pixel):
        for number in pixel_locations:
            floored = ceil(number)
            if pixel == floored or floored <= curr_stack + 1:
                return number
        return None

    for i in range(max_pixels):
        movePixel = getMovePixel(i)
        if i < curr_stack:
            val.append(255)
            continue

        if movePixel is not None:
            val.append(255)
            if i <= curr_stack + 1:
                curr_stack += 1
                index = pixel_locations.index(movePixel)

                del pixel_locations[index]
            continue

        val.append(0)
    return np.array([val, val, val])
