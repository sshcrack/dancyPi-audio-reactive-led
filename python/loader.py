import sys
import threading
import time
import traceback

import os
import os.path as path
import config
import json
from base.controller import GeneralController
from base.visualization import microphone
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
minimalMode = "--minimal" in sys.argv


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


def getAliveThreads():
    threadNames = []
    for e in threads:
        if e.is_alive():
            threadNames.append(e.name)
    return threadNames


def getMatchingController(controller_name: str):
    for x in controllerList:
        if x.__name__ == controller_name:
            return x
    return None


def measureMicThread():
    if not microphone.isRunning():
        print("Starting microphone service...")
        microphone.start()
    while not exitSignal:
        out = measureMic()
        for key in controllers:
            controllers[key].mel = out
    print("Stopping microphone...")
    microphone.stop()


def measureMic():
    raw = microphone.read()
    return microphone.microphone_update(raw)


for relativeDevPath in devicesFiles:
    print(f"Starting thread for device {relativeDevPath}")
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
    thread = Thread(target=lambda: runController(c, deviceId), name=f"CONTROLLER-{deviceId}")
    threads.append(thread)
    thread.start()

measureThread = Thread(target=measureMicThread)
measureThread.start()

server = None if minimalMode else MainHTTPServer(controllers)
if not minimalMode:
    print("Starting Main Server...")
    server.serve(config.BIND_ADDRESS, config.PORT)
try:
    while someThreadsRunning():
        pass
except KeyboardInterrupt:
    pass
finally:
    print("Sending exit signal...")
    exitSignal = True
    measureThread.join()
    if not minimalMode:
        print("Shutting server down...")
        server.shutdown()

    while someThreadsRunning():
        print(f"Still some controllers running: {getAliveThreads()}")
        time.sleep(1.5)
    while True:
        currRunning = threading.enumerate()
        if len(currRunning) == 0:
            break

        print(f"Some threads running: {currRunning}")