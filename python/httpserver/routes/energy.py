from http.server import BaseHTTPRequestHandler
from typing import  List

from httpserver.currVars import setConfig
from tools.tools import check_float, isInt


def onEnergySpeed(_server: BaseHTTPRequestHandler, params: List[str]):
    bright_bool = params.get("brightness")
    speed_bool = params.get("speed")
    sensitivity_str = params.get("sensitivity")

    if bright_bool != None and len(bright_bool) != 0:
        bright_bool = bright_bool[0]


    if speed_bool != None and len(speed_bool) != 0:
        speed_bool = speed_bool[0]

    if sensitivity_str != None and len(sensitivity_str) != 0:
        sensitivity_str = sensitivity_str[0]

    bright_res = None
    speed_res = None

    if bright_bool == "true":
        bright_res = True
    elif bright_bool == "false":
        bright_res = False
    else:
        return (400, {
            "error": "Brightness can either be 'true' or 'false'"
        })

    if speed_bool == "true":
        speed_res = True
    elif speed_bool == "false":
        speed_res = False
    else:
        return (400, {
            "error": "Speed can either be 'true' or 'false'"
        })

    if not check_float(sensitivity_str):
        return (400, {
            "error": f"Sensitivity can not be {sensitivity_str} (not valid float)"
        })

    setConfig("energy_brightness", bright_res)
    setConfig("energy_speed", speed_res)
    setConfig("energy_sensitivity", float(sensitivity_str))

    return (200, {
        "success": True,
        "mode": bright_bool
    })