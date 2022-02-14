import gesture.grove_gesture_sensor as grove_gesture_sensor
import RPi.GPIO as GPIO
from threading import Thread
import time

enabled = True
shouldRun = True

g=grove_gesture_sensor.gesture()

LED_PIN = 4
GPIO.setmode(GPIO.BCM)

def hasGesture():
        gest=g.return_gesture()
        return gest != 0

def ledUpdate():
    global enabled
    GPIO.output(LED_PIN, enabled)

def measureThread():
    print("Initializing gesture...")

    g.init()
    GPIO.setup(LED_PIN, GPIO.OUT)

    global enabled, shouldRun
    print(f"Should run {shouldRun}")

    ledUpdate()
    while shouldRun:
        if hasGesture():
            enabled =  not enabled
            print(f"Setting enabled to {enabled}")
            ledUpdate()

        time.sleep(.1)
    print("Exiting thread...")

def isEnabled():
    global enabled
    return enabled

def stop():
    global shouldRun
    shouldRun = False

thread1 = Thread(target=measureThread, daemon=False)
thread1.start()
