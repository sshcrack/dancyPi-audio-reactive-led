import numpy as np
import tools.tools as tools
from base.GeneralMode import GeneralMode
from tools.validators import validate_float
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from base.controller import GeneralController


def getMax(arr):
    maxVal = arr[0]
    for x in arr:
        if x > maxVal:
            maxVal = x

    return maxVal


class RainbowMode(GeneralMode):
    def __init__(self, controller: "GeneralController"):
        super().__init__({
            "rainbow_speed": 1
        }, {
            "required_vars": {
                "rainbow_speed": {
                    "func": validate_float("speed"),
                    "type": "float",
                    "sug_min": 0,
                    "sug_max": 5
                }
            }
        }, controller)
        self.rgb_index = 0

    def run(self, data):
        r, g, b = data
        speed = self.config.get("rainbow_speed", 1)
        if speed is None:
            speed = self.config.getGeneralSpeed()

        deltaTime = self.timer.getDelta()

        for i in range(len(r)):
            maxVal = getMax([r[i], g[i], b[i]])
            self.rgb_index += deltaTime * speed
            local_led_index = int(self.rgb_index + i)
            values = np.array(tools.wheel(local_led_index)) / 255

            if self.rgb_index >= 255:
                self.rgb_index = 0

            r[i] = values[0] * maxVal
            g[i] = values[1] * maxVal
            b[i] = values[2] * maxVal

        return np.array([r, g, b])
