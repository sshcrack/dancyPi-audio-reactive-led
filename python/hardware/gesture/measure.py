import hardware.gesture.grove_gesture_sensor as grove_gesture_sensor
from threading import Thread
import time
from config import STATUS_LED_PIN, GESTURE_SENSOR_ENABLED
from httpserver.currVars import getConfig, setConfig
shouldRun = True

if GESTURE_SENSOR_ENABLED:
        g=grove_gesture_sensor.gesture()


def hasGesture():
        gest=g.return_gesture()
        return gest != 0

def measureThread():
    print("Initializing gesture...")
    if not GESTURE_SENSOR_ENABLED:
        return

    g.init()

    global shouldRun
    print(f"Should run {shouldRun}")

    while shouldRun:
        if hasGesture():
            enabled = not isEnabled()

            setConfig("enabled", enabled)
            print(f"Setting enabled to {enabled}")

        time.sleep(.1)

    print("Exiting thread...")

def isEnabled():
    return getConfig("enabled")

def stop():
    global shouldRun
    shouldRun = False

thread1 = Thread(target=measureThread, daemon=True)
thread1.start()
