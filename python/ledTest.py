# from base.controller import GeneralController
import numpy as np

from controller.shelf.modes.shelfAnimator import ShelfAnimatorMode
from controller.shelf.shelfController import ShelfController
from controller.shelf.shelfTools import mappingToIndex, mappings

controller = ShelfController("shelf", gui=True)  # {} {}, gui=True)

# try:
#    m = ShelfAnimatorMode(controller)
#    while True:
#        x = m.run(None)
#        x = controller.postProcessPixels(x)
#        controller.timer.update()
#        controller.pixels = x
#        controller.updateLeds()
# except KeyboardInterrupt:
#    controller.shutdown()
#    exit(0)

offsets = []
offset = 0

for mapping in mappings:
    f, s = mapping
    diff = s - f

    offsets.append([offset, offset + diff])
    offset += diff + 1

try:
    while True:
        try:
            pixels = np.tile(0, controller.device.N_PIXELS)
            x = int(input("Index"))
            f, s = offsets[x]

            print("From", f, "to", s)
            diff = s - f
            for i in range(diff):
                pixels[f + i] = 255
            controller.pixels = controller.postProcessPixels(np.array([pixels, pixels, pixels]))
            controller.updateLeds()
        except (ValueError, IndexError):
            pass
except KeyboardInterrupt:
    print("Exit")
    controller.shutdown()
    exit(-1)

# try:
#    while True:
#        try:
#            pixels = np.tile(0, controller.device.N_PIXELS)
#            minRange = int(input("Min Range Range"))
#            maxRange = int(input("Max Range"))
#            for i in range(minRange, maxRange):
#                pixels[i] = 255
#
#            controller.pixels = controller.postProcessPixels(np.array([pixels, pixels, pixels]))
#            controller.updateLeds()
#        except ValueError:
#            pass
# except KeyboardInterrupt:
#    controller.shutdown()
