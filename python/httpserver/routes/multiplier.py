from typing import List
from http.server import BaseHTTPRequestHandler

from httpserver.currVars import setMultiplier
from tools.tools import check_float

def onMultiplier(server: BaseHTTPRequestHandler, params: List[str]):
    multiplier = params.get("multiplier")

    if multiplier != None and len(multiplier) != 0:
        multiplier: str = multiplier[0]

    if not check_float(multiplier):
        return (400,
                {
                    "error": f"Invalid multiplier {multiplier}"
                })

    multiplier = float(multiplier)
    setMultiplier(multiplier)

    return (200, {
        "success": True,
        "speed": multiplier
    })