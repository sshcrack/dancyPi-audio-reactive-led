from prodict import Prodict
from os import path, getcwd
import json
from typing import Optional


class GeneralLEDConfig(Prodict):
    DEVICE: str
    N_PIXELS: int
    CONTROLLER: str
    SOFTWARE_GAMMA_CORRECTION: Optional[bool]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.SOFTWARE_GAMMA_CORRECTION = False


class RPIConfig(GeneralLEDConfig):
    LED_PIN: int
    LED_FREQ_HZ: Optional[int]
    LED_DMA: Optional[int]
    LED_INVERT: Optional[bool]
    BRIGHTNESS: Optional[int]
    SOFTWARE_GAMMA_CORRECTION: Optional[bool]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.SOFTWARE_GAMMA_CORRECTION = True
        self.BRIGHTNESS = 255
        self.LED_INVERT = False
        self.LED_DMA = 5
        self.LED_FREQ_HZ = 800000


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


ConfigMappings = {
    "pi": RPIConfig,
    "esp8266": ESPConfig,
    "blinkstick": BlinkstickConfig
}
