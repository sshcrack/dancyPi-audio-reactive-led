from typing import List
import json


data = {
    "mode": "spectrum",
    "filter_mode": "hex",
    "speed": 1,
    "multiplier": 1,
    "stack_concurrent": 1,
    "stack_speed": 1,
    "scanner_size": 10,
    "scanner_shadow": 2,
    "filter_gradient": [
        [0, [0, 0, 0]],
        [1, [255, 255, 255]]
    ],
    "energy_brightness": False,
    "energy_speed": False,
    "energy_multiplier": 1,
    "energy_sensitivity": 1
}


def load():
    global data

    f = None
    try:
        f = open("vars.json", "r")
        raw = f.read()
        data = json.loads(raw)
    except (json.JSONDecodeError, FileNotFoundError):
        print("Could not parse json file. Staying with default.")

    if f != None and not f.closed:
        f.close()


def save():
    global data
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
        speed *= data["energy_multiplier"]

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
    data["filter_gradient"] = gradient


def getGradient():
    global data
    return data["filter_gradient"]

def getConfig(key: str):
    global data
    return data.get(key)

    
def setConfig(key: str, val):
    global data
    data[key] = val