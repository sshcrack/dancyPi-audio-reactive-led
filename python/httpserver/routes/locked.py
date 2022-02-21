from http.server import BaseHTTPRequestHandler
from typing import  List

from httpserver.currVars import getConfig, setConfig


def onLocked(_server: BaseHTTPRequestHandler, params: List[str]):
    locked_str = params.get("locked")
    
    if locked_str != None and len(locked_str) != 0:
        locked_str = locked_str[0]

    if locked_str == "true":
        setConfig("locked", True)
    elif locked_str == "false":
        setConfig("locked", False)
    else:
        return (400, {
            "error": "Locked has to be either 'true' or 'false'"
        })

    locked = getConfig("locked")
    return (200, {
        "result": f"Changed value to {locked}"
    })