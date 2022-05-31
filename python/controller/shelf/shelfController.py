from controller.ledstrip.ledStripController import LEDStripController
import numpy as np

from controller.shelf.modes.shelfAnimator import ShelfAnimatorMode
from controller.shelf.shelfTools import mappingToIndex

modes = {
    'shelf_animator': ShelfAnimatorMode
}


class ShelfController(LEDStripController):
    def __init__(self, deviceId: str, gui=False):
        super().__init__(deviceId, gui, additionalModes=modes)

    def postProcessPixels(self, data: np.ndarray):
        mapped = np.copy(data)
        r, g, b = data
        for i in range(len(r)):
            aI = mappingToIndex(i)
            mapped[0][aI] = r[i]
            mapped[1][aI] = g[i]
            mapped[2][aI] = b[i]

        return mapped
