from http.server import BaseHTTPRequestHandler
from typing import  List

from httpserver.currVars import getConfig, setConfig


def onEnabled(_server: BaseHTTPRequestHandler, params: List[str]):
    enabled_str = params.get("enabled")
    
    if enabled_str != None and len(enabled_str) != 0:
        enabled_str = enabled_str[0]

    if enabled_str == "true":
        setConfig("enabled", True)
    elif enabled_str == "false":
        setConfig("enabled", False)
    else:
        return (400, {
            "error": "Enabled has to be either 'true' or 'false'"
        })

    enabled = getConfig("enabled")
    return (200, {
        "result": f"Changed value to {enabled}"
    })