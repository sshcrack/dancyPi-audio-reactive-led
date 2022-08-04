import numpy as np
from base.GeneralMode import GeneralMode
from tools.validators import validate_float
from typing import TYPE_CHECKING
import json

if TYPE_CHECKING:
    from base.controller import GeneralController

f = open("base/filters/rainbow.json", "r")
rainbow = np.array(json.loads(f.read()))
f.close()


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
        avg = np.average(data, axis=0)

        length = len(r)

        rgbIndices = np.full(length, deltaTime * speed)
        multiplyArr = np.arange(1, length + 1).astype(float)

        rgbIndices = np.multiply(rgbIndices, multiplyArr) + self.rgb_index
        self.rgb_index = rgbIndices[-1] % 255
        rgbIndices = np.add(rgbIndices, multiplyArr - 1)

        rgbIndices = rgbIndices.astype(int)
        rgbIndices = np.remainder(rgbIndices, 255)
        rgbIndices = rainbow.take(rgbIndices, axis=0)

        r = rgbIndices[:, 0] * avg / 255
        g = rgbIndices[:, 1] * avg / 255
        b = rgbIndices[:, 2] * avg / 255
        return np.array([r, g, b])
