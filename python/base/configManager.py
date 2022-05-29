from typing import TypeVar
import json
import os
from pathlib import Path as Pathlib
from os import path

cwd = os.getcwd()
storage_path = path.join(cwd, "storage")

path = Pathlib(storage_path)
if not path.exists() or not path.is_dir():
    path.mkdir(parents=True)

T = TypeVar("T")


class ConfigManager:
    storage = {}

    def __init__(self, storage_id: str, defaults=None):
        if defaults is None:
            defaults = {
                "speed": 1,
                "multiplier": 1,
                "mode": "spectrum",
                "filter_mode": "normal",
                "energy_brightness": False,
                "energy_brightness_mult": 1,
                "energy_speed": False,
                "energy_speed_mult": 1,
                "energy_curr": 1,
                "energy_sensitivity": 1,
                "enabled": True,
                "locked": False
            }

        self.config_path = path.join(storage_path, f"{storage_id}.json")
        f = None
        try:
            print("Loading config with id", storage_id)
            f = open(self.config_path, "r")
            raw = f.read()
            self.storage = {**defaults, **json.loads(raw)}
        except (json.JSONDecodeError, FileNotFoundError):
            print(f"Could not parse json file ({self.config_path}). Staying with default.")
            self.storage = defaults

        if f is not None and not f.closed:
            f.close()

    def save(self):
        with open(self.config_path, "w") as f:
            f.write(json.dumps(self.storage))

    def get(self, key: str, default: T = None):
        if key not in self.storage.keys():
            return default

        if key == "enabled" and self.get("locked"):
            return

        return self.storage[key]

    def set(self, key: str, value: T):
        self.storage[key] = value

    def setGeneralSpeed(self, speed: float):
        self.set("speed", speed)

    def getGeneralSpeed(self):
        energy_speed = self.get("energy_speed", 1)
        speed = self.get("speed", 1)
        if energy_speed:
            speed *= self.get("energy_curr") * self.get("energy_speed_mult")

        return speed

    def getAll(self):
        return self.storage

    def setFilterMode(self, filter_mode: str):
        self.storage["filter_mode"] = filter_mode

    def getFilterMode(self):
        return self.storage["filter_mode"]

    def setMode(self, mode: str):
        self.storage["mode"] = mode

    def getMode(self):
        return self.storage["mode"]

    def setLock(self, locked: bool):
        self.storage["locked"] = locked

    def isLocked(self):
        return self.storage["locked"]