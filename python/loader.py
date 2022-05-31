import sys
import traceback

import os
import os.path as path
import config
import json
from base.controller import GeneralController
from controller.ledstrip.ledStripController import LEDStripController
from threading import Thread
from base.hardware.configDict import deviceConfigLocation
from controller.shelf.shelfController import ShelfController

from httpserver.main.server import MainHTTPServer

threads = []
exitSignal = False

controllers = {}
devicesFiles = os.listdir(deviceConfigLocation)

controllerList = [
    LEDStripController,
    ShelfController
]
isGui = "--gui" in sys.argv


def runController(controller: GeneralController, devId: str):
    try:
        while not controller.shouldExit and not exitSignal:
            controller.run()
    except Exception:
        print(f"Error for controller {devId}")
        traceback.print_exc()
    finally:
        print("Shutting down controller", devId)
        controller.shutdown()


def someThreadsRunning():
    for e in threads:
        if e.is_alive():
            return True
    return False


def getMatchingController(controller_name: str):
    for c in controllerList:
        if c.__name__ == controller_name:
            return c
    return None


for relativeDevPath in devicesFiles:
    print(f"Starting thread for device")
    devPath = path.join(deviceConfigLocation, relativeDevPath)

    devFile = open(devPath, "r")
    devRaw = devFile.read()
    devFile.close()

    devJson = json.loads(devRaw)
    if devJson.get("DISABLED"):
        continue

    controller = devJson["CONTROLLER"]

    deviceId = path.basename(devPath).rsplit(".", maxsplit=1)[0]
    matching = getMatchingController(controller)
    if matching is None:
        print("Could not find matching controller for", deviceId, "continuing...")
        continue

    c = matching(deviceId, gui=isGui)
    controllers[deviceId] = c
    thread = Thread(target=lambda: runController(c, deviceId))
    threads.append(thread)
    thread.start()

server = MainHTTPServer(controllers)
server.serve(config.BIND_ADDRESS, config.PORT)

try:
    while someThreadsRunning():
        pass
except KeyboardInterrupt:
    pass
finally:
    print("Sending exit signal...")
    exitSignal = True
    server.shutdown()
