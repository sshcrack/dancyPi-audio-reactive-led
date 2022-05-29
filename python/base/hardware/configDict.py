from prodict import Prodict
from os import path, getcwd
import json


class GeneralLEDConfig(Prodict):
    DEVICE_NAME: str
    N_PIXELS: int
    SOFTWARE_GAMMA_CORRECTION = False
    enabled = True


class RPIConfig(GeneralLEDConfig):
    LED_PIN: int
    N_PIXELS: int
    LED_FREQ_HZ = 800000
    LED_DMA = 5
    LED_INVERT = False
    BRIGHTNESS = 255
    SOFTWARE_GAMMA_CORRECTION = True


class ESPConfig(GeneralLEDConfig):
    UDP_PORT: str
    UDP_IP: str


class BlinkstickConfig(GeneralLEDConfig):
    pass


cwd = getcwd()
deviceConfigLocation = path.join(cwd, "device_config")


def loadDeviceConfig(devId: str) -> GeneralLEDConfig:
    configFile = path.join(deviceConfigLocation, f"{devId}.json")
    if not path.exists(configFile):
        raise FileNotFoundError("Could not find device configuration file" +
                                f"for device with id {devId} and config file {configFile}.")

    f = open(configFile, "r")
    raw = f.read()
    f.close()

    return Prodict.from_dict(json.loads(raw))
