from math import ceil, floor

import numpy as np
from base.controller import GeneralController
from base.GeneralMode import GeneralMode
from tools.validators import validate_int, validate_float


class StackMode(GeneralMode):
    def __init__(self, controller: GeneralController):
        super().__init__({
            "stack_concurrent": 6,
            "stack_speed": 1
        }, {
            "visualizer": False,
            "filters": True,
            "required_vars": {
                "stack_concurrent": {
                    "sug_max": 30,
                    "sug_min": 1,
                    "func": validate_int("concurrent", 1),
                    "type": "int",
                    "min": 1
                },
                "stack_speed": {
                    "sug_max": 15,
                    "sug_min": 0,
                    "min": 0,
                    "func": validate_float("speed"),
                    "type": "float"
                }
            }
        }, controller)

        self.curr_stack = 0
        self.pixel_locations = []
        self.animating_out = False
        self.animating_status = 0

    def run(self, mel):
        general_speed_modifier = .25

        dev = self.device
        config = self.config

        delta = self.timer.getDelta()
        speed = config.getGeneralSpeed()

        max_pixels = dev.N_PIXELS
        concurrent = config.get("stack_concurrent")
        stack_speed = config.get("stack_speed")

        if self.curr_stack >= max_pixels:
            curr_stack = 0
            self.pixel_locations = []
            self.animating_out = True

        if self.animating_out:
            channel = []
            pixels = floor((1 - self.animating_status) * max_pixels)
            self.animating_status += delta * speed * general_speed_modifier

            if self.animating_status > 1:
                self.animating_out = False
                self.animating_status = 0
            else:
                for i in range(max_pixels):
                    if pixels >= i:
                        channel.append(255)
                        continue
                    channel.append(0)

                return np.array([channel, channel, channel])

        pixel_length = len(self.pixel_locations)
        if pixel_length != concurrent:
            diff = concurrent - pixel_length
            if diff != 0:
                single_size = 1 / concurrent
                for i in range(diff):
                    self.pixel_locations.append(max_pixels + single_size * i * max_pixels)

        for i in range(len(self.pixel_locations)):
            curr = self.pixel_locations[i]
            curr -= delta * speed * general_speed_modifier * stack_speed * max_pixels
            if curr >= 0:
                self.pixel_locations[i] = curr
            else:
                self.pixel_locations[i] = 0

        val = []

        def getMovePixel(pixel):
            for number in self.pixel_locations:
                floored = ceil(number)
                if pixel == floored or floored <= curr_stack + 1:
                    return number
            return None

        for i in range(max_pixels):
            movePixel = getMovePixel(i)
            if i < self.curr_stack:
                val.append(255)
                continue

            if movePixel is not None:
                val.append(255)
                if i <= self.curr_stack + 1:
                    self.curr_stack += 1
                    index = self.pixel_locations.index(movePixel)

                    del self.pixel_locations[index]
                continue

            val.append(0)
        return np.array([val, val, val])
