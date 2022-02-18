import hardware.gesture.grove_gesture_sensor as grove_gesture_sensor
import RPi.GPIO as GPIO
from threading import Thread
import time
from config import STATUS_LED_PIN
from httpserver.currVars import getConfig, setConfig

shouldRun = True

g=grove_gesture_sensor.gesture()

GPIO.setmode(GPIO.BCM)

def hasGesture():
        gest=g.return_gesture()
        return gest != 0

def ledUpdate(enabled: bool):
    GPIO.output(STATUS_LED_PIN, enabled)

def measureThread():
    print("Initializing gesture...")

    g.init()
    GPIO.setup(STATUS_LED_PIN, GPIO.OUT)

    global shouldRun
    print(f"Should run {shouldRun}")

    ledUpdate(isEnabled())
    while shouldRun:
        if hasGesture():
            enabled = not isEnabled()

            setConfig("enabled", enabled)
            print(f"Setting enabled to {enabled}")
            ledUpdate(enabled)

        time.sleep(.1)

    GPIO.cleanup()
    print("Exiting thread...")

def isEnabled():
    return getConfig("enabled")

def stop():
    global shouldRun
    shouldRun = False

thread1 = Thread(target=measureThread, daemon=False)
thread1.start()
