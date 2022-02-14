
from typing import List
import json


data = {
    "mode": "spectrum",
    "filter_mode": "hex",
    "speed": 1,
    "filter_gradient": [
        [0, [0, 0, 0]],
        [1, [255, 255, 255]]
    ]
}


def load():
    global data
    f = open("config.json", "r")
    raw = f.read()

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        print("Could not parse json file. Going to default.")

    f.close()


def save():
    global data
    f = open("config.json", "w")
    f.write(json.dumps(data))

    f.close()


def setFilterMode(new_mode: str):
    global data
    data["filter_mode"] = new_mode


def getFilterMode():
    global data
    return data["filter_mode"]


def setMode(new_mode: str):
    global data
    data["mode"] = new_mode


def getMode():
    global data
    return data["mode"]


def setGeneralSpeed(new_speed: float):
    global data
    data["speed"] = new_speed


def getGeneralSpeed():
    global data
    return data["speed"]


def setGradient(new_gradient: List[List]):
    global data
    data["filter_gradient"] = new_gradient


def getGradient():
    global data
    return data["filter_gradient"]
