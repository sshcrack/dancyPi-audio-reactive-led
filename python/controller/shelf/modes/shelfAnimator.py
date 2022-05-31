import math

import numpy as np

from base.GeneralMode import GeneralMode
from base.controller import GeneralController
from controller.shelf.shelfTools import mappings
from tools.validators import validate_float


class ShelfAnimatorMode(GeneralMode):
    def __init__(self, controller: GeneralController):
        super().__init__({
            "shelf_animator_speed": 1
        }, {
            "visualizer": False,
            "filters": True,
            "required_vars": {
                "shelf_animator_speed": {
                    "sug_max": 100,
                    "sug_min": 0,
                    "func": validate_float("speed", 0),
                    "type": "float",
                    "min": 0
                }
            }
        }, controller)
        self.animation_index = 0.0001

        self.offsets = []
        self.forward = True
        offset = 0

        for mapping in mappings:
            f, s = mapping
            diff = s - f

            self.offsets.append([offset, offset + diff])
            offset += diff + 1

    def run(self, _):
        length = len(self.offsets)
        speed = self.config.get("shelf_animator_speed")
        delta = self.timer.getDelta()

        prevCurr = math.floor(self.animation_index % length)
        self.animation_index += delta * speed

        percentage = self.animation_index - math.floor(self.animation_index)

        currIndex = math.floor(self.animation_index % length)
        if not self.forward:
            currIndex = length - currIndex

        if prevCurr == len(self.offsets) and currIndex == 0:
            self.forward = not self.forward

        alpha = np.tile(0, self.device.N_PIXELS)

        fCurr, sCurr = self.offsets[currIndex]

        light = 255 - int(math.fabs(255 * (0.5 - percentage) * 2))
        for i in range(sCurr - fCurr):
            alpha[fCurr + i] = light

        return np.array([alpha, alpha, alpha])
