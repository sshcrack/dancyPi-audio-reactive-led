from http.server import BaseHTTPRequestHandler
import json
from typing import Any, List
import led.tools as tools
import re

from httpserver.currVars import setFilterMode, setGradient

availableModes = ["hex", "normal", "rainbow"]


def isNotNumber(s: Any):
    return not str(s).isnumeric()

def isNotColorHex(s: str):
    return not re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', str(s))


def onFilter(_server: BaseHTTPRequestHandler, params: List[str]):
    mode = params.get("mode")
    gradient: List[str] = params.get("gradient")
    gradient_hex: List[str] = params.get("gradient_hex")

    if mode != None and len(mode) != 0:
        mode = mode[0]
        
    if gradient != None and len(gradient) != 0:
        gradient = json.loads(gradient[0])

    if gradient_hex != None and len(gradient_hex) != 0:
        gradient_hex = json.loads(gradient_hex[0])

    if mode not in availableModes:
        return (400,
                {
                    "error": f"Invalid mode valid modes are {availableModes}",
                    "mode": mode
                })

    setFilterMode(mode)
    if mode == "hex":
        if gradient == None or len(gradient) == 0:
            return (400,
                    {
                        "error": "When using mode hex a gradient step array has to be given"
                    })

        if gradient_hex == None or len(gradient_hex) == 0:
            return (400,
                    {
                        "error": "When using mode hex a gradient hex array has to be given"
                    })

        if len(gradient) != len(gradient_hex):
            return (400,
                    {
                        "error": f"Gradient hex array and step array are not at same size ({len(gradient)},{len(gradient_hex)}"
                    })


        any_non_numbers = list(map(isNotNumber, gradient))
        any_non_hex = list(map(isNotColorHex, gradient_hex))

        if any(any_non_numbers):
            return (400,
                    {
                        "error": f"One of {gradient} is not a valid number {json.dumps(any_non_numbers)}"
                    })

        if any(any_non_hex):
            return (400,
                    {
                        "error": f"One of {gradient_hex} is not a valid hex color {json.dumps(any_non_hex)}"
                    })


        gradient_rgb = list(map(tools.hex_to_rgb, gradient_hex))
        gradient_data = []
        for i in range(len(gradient)):
            gradient_data.append([ gradient[i], gradient_rgb[i] ])

        print(f"Gradient data set to {gradient_data}")
        setGradient(gradient_data)

    return (200, {
        "success": True,
        "mode": mode
    })