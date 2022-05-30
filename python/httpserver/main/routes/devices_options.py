import typing
from typing import Dict, TYPE_CHECKING, List, Union

from base.hardware.configDict import ConfigMappings

if TYPE_CHECKING:
    from base.controller import GeneralController


def onDevicesOptions(controllers: Dict[str, "GeneralController"], params: List[str]):
    info = {}
    keys = list(ConfigMappings.keys())
    for key in keys:
        el = ConfigMappings[key]
        constructed = el()

        attrTypes = el.attr_types()
        attrKeys = list(attrTypes.keys())
        attrList = {}
        for attrKey in attrKeys:
            aType = attrTypes[attrKey]
            isOptional = typing.get_origin(aType) == Union

            standardInfo = {
                "name": attrKey,
            }
            if isOptional:
                optionalType = typing.get_args(aType)[0]
                defaultVal = constructed[attrKey]
                attrList[attrKey] = {
                    **standardInfo,
                    "type": optionalType.__name__,
                    "optional": True,
                    "default": defaultVal
                }
            else:
                attrList[attrKey] = {
                    **standardInfo,
                    "type": aType.__name__
                }
        info[key] = attrList
    return 200, info
