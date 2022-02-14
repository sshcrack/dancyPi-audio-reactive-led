from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler

from httpserver.currVars import setMode

availableModes = [
    "spectrum",
    "energy",
    "scroll"
]


def onSetMode(server: BaseHTTPRequestHandler):
    parsed = urlparse(server.path)
    params = parse_qs(parsed.query)
    mode = params.get("mode")

    if mode != None and len(mode) != 0:
        mode = mode[0]

    if mode not in availableModes:
        return (400,
                {
                    "error": f"Invalid mode valid modes are {availableModes}",
                    "mode": mode
                })

    setMode(mode)
    return (200, {
        "success": True,
        "mode": mode
    })
