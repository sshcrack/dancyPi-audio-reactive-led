from math import floor
import numpy as np
from base.controller import GeneralController
from base.GeneralMode import GeneralMode
from tools.validators import validate_float, validate_int


class ScannerMode(GeneralMode):
    def __init__(self, controller: GeneralController):
        super().__init__({
            "scanner_size": 1,
            "scanner_shadow": 1,
            "scanner_speed": 1
        }, {
            "visualizer": False,
            "filters": True,
            "required_vars": {
                "scanner_size": {
                    "sug_max": 30,
                    "sug_min": 1,
                    "func": validate_int("size", 1),
                    "type": "int",
                    "min": 1
                },
                "scanner_shadow": {
                    "sug_max": 15,
                    "sug_min": 0,
                    "min": 0,
                    "func": validate_float("shadow"),
                    "type": "float"
                },
                "scanner_speed": {
                    "sug_max": 2,
                    "sug_min": 0,
                    "min": 0,
                    "func": validate_float("speed"),
                    "type": "float"
                }
            }
        }, controller)

        self.max_pixels = self.device.N_PIXELS
        self.center_pos = self.max_pixels / 2
        self.direction = True
        print("Initial", self.center_pos)

    def run(self, _):
        delta = self.timer.getDelta()
        speed = self.config.getGeneralSpeed()

        full_bright = self.config.get("scanner_size", 1)
        shadow_size = self.config.get("scanner_shadow", 1)
        scannerSpeed = self.config.get("scanner_speed", 1)

        # 2 times for both sides
        total_size = full_bright + 2 * shadow_size
        half_size = total_size / 2

        if self.center_pos <= half_size:
            self.direction = 1
        elif self.center_pos >= self.max_pixels - half_size:
            self.direction = -1

        self.center_pos += delta * speed * 150 * self.direction * scannerSpeed
        channel = []

        min_shadow = self.center_pos - shadow_size
        max_shadow = self.center_pos + shadow_size
        for i in range(self.max_pixels):
            if not (min_shadow <= i <= max_shadow):
                channel.append(0)
                continue

            # could also be min_shadow
            distance = 1 - abs((i - self.center_pos) / shadow_size)
            brightness = floor(min(distance * 255, 255))

            channel.append(brightness)

        return np.array([channel, channel, channel])


