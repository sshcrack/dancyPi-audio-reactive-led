from typing import List
import json
from config import STATUS_LED_PIN

status_led_available = False
try:
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)
    status_led_available = True
except Exception as e:
    print("Could not import RPi, disabling status led")


def ledUpdate(enabled: bool):
    if status_led_available:
        GPIO.output(STATUS_LED_PIN, enabled)


data = {
    "mode": "spectrum",
    "filter_mode": "hex",
    "speed": 1,
    "multiplier": 1,
    "stack_concurrent": 1,
    "stack_speed": 1,
    "scanner_size": 10,
    "scanner_shadow": 2,
    "hex_gradient": [
        [0, [0, 0, 0]],
        [1, [255, 255, 255]]
    ],
    "energy_brightness": False,
    "energy_brightness_mult": 1,
    "energy_speed": False,
    "energy_speed_mult": 1,
    "energy_curr": 1,
    "energy_sensitivity": 1,
    "rainbow_speed": 1,
    "enabled": True,
    "locked": False
}

if STATUS_LED_PIN is not None and status_led_available:
    GPIO.setup(STATUS_LED_PIN, GPIO.OUT)


def load():
    global data

    f = None
    print("Loading variables...")
    try:
        f = open("vars.json", "r")
        raw = f.read()
        data = json.loads(raw)
    except (json.JSONDecodeError, FileNotFoundError):
        print("Could not parse json file. Staying with default.")

    if f is not None and not f.closed:
        f.close()

    if STATUS_LED_PIN is not None:
        ledUpdate(data.get("enabled"))


def save():
    global data
    print("Saving variables...")
    f = open("vars.json", "w")
    f.write(json.dumps(data))

    f.close()


def setFilterMode(filter_mode: str):
    global data
    data["filter_mode"] = filter_mode


def getFilterMode():
    global data
    return data["filter_mode"]


def setMode(mode: str):
    global data
    data["mode"] = mode


def getMode():
    global data
    return data["mode"]


def setGeneralSpeed(speed: float):
    global data
    data["speed"] = speed


def getGeneralSpeed():
    global data
    energy_speed = data["energy_speed"]
    speed = data["speed"]
    if energy_speed:
        speed *= data["energy_curr"] * data["energy_speed_mult"]

    return speed


def setSpeedMultiplier(mult: float):
    global data
    data["energyspeed_multiplier"] = mult


def setMultiplier(multiplier: float):
    global data
    data["multiplier"] = multiplier


def getMultiplier():
    global data
    return data["multiplier"]


def setGradient(gradient: List[List]):
    global data
    data["hex_gradient"] = gradient


def getGradient():
    global data
    return data["hex_gradient"]


def getConfig(key: str, default=None):
    global data
    if default is not None and key not in data.keys():
        return default

    return data.get(key)


def setConfig(key: str, val):
    global data

    if key == "enabled":
        if data.get("locked"):
            return

        if STATUS_LED_PIN is not None:
            ledUpdate(val)
    data[key] = val


def getAllVars():
    global data
    return data


def cleanupGPIO():
    if not status_led_available:
        return
    print("Cleaning up GPIO...")
    GPIO.cleanup()
