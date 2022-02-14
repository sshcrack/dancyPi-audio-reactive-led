from typing import List
from http.server import BaseHTTPRequestHandler
from modes import modeKeys

from httpserver.currVars import setMode

def onSetMode(server: BaseHTTPRequestHandler, params: List[str]):
    mode = params.get("mode")

    if mode != None and len(mode) != 0:
        mode = mode[0]

    if mode not in modeKeys:
        return (400,
                {
                    "error": f"Invalid mode valid modes are {modeKeys}",
                    "mode": mode
                })

    setMode(mode)
    return (200, {
        "success": True,
        "mode": mode
    })
