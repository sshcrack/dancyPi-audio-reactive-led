from http.server import BaseHTTPRequestHandler
from typing import  List

from httpserver.currVars import setConfig


def onEnergySpeed(_server: BaseHTTPRequestHandler, params: List[str]):
    set_bool = params.get("set")

    if set_bool != None and len(set_bool) != 0:
        set_bool = set_bool[0]

    if set_bool == "true":
        setConfig("energyspeed", True)
    elif set_bool == "false":
        setConfig("energyspeed", False)
    else:
        return (400, {
            "error": "Set can either be 'true' or 'false'"
        })

    return (200, {
        "success": True,
        "mode": set_bool
    })