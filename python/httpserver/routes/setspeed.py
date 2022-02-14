from typing import List
from http.server import BaseHTTPRequestHandler

from httpserver.currVars import setGeneralSpeed, setMode

def onSetSpeed(server: BaseHTTPRequestHandler, params: List[str]):
    speed = params.get("speed")

    if speed != None and len(speed) != 0:
        speed: str = speed[0]

    if speed.isnumeric():
        return (400,
                {
                    "error": f"Invalid speed {speed}"
                })

    speed = float(speed)

    setGeneralSpeed(speed)
    return (200, {
        "success": True,
        "speed": speed
    })
