from typing import Dict, TYPE_CHECKING, List

if TYPE_CHECKING:
    from base.controller import GeneralController


def onDevicesList(controllers: Dict[str, "GeneralController"], params: List[str]):
    devices = {}
    for key in list(controllers.keys()):
        c = controllers.get(key)
        devices[key] = {
            "name": c.deviceId,
            "device": c.device,
            "config": c.config.storage
        }
    return 200, devices
