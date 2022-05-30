import json
import sys
from http.server import BaseHTTPRequestHandler

from httpserver.base import ThreadedHTTPServer
from tools.interfaces import getIPs
from threading import Thread
from urllib.parse import parse_qs, urlparse
from httpserver.api.routes.available import onAvailable
from httpserver.api.routes.enabled import onEnabled
from httpserver.api.routes.energy import onEnergy
from httpserver.api.routes.locked import onLocked
from httpserver.api.routes.multiplier import onMultiplier
from httpserver.api.routes.setmode import onSetMode
from httpserver.api.routes.filter import onFilter
from httpserver.api.routes.setspeed import onSetSpeed
from httpserver.api.routes.vars import onVars
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from base.controller import GeneralController

AVAILABLE_ROUTES = [
    "setmode",
    "enabled",
    "locked",
    "speed",
    "filter",
    "multiplier",
    "energy",
    "vars",
    "available"
]


class APIServerHandler(BaseHTTPRequestHandler):
    def __init__(self, controller: "GeneralController", *args, **kwargs):
        self.controller = controller
        super().__init__(*args, **kwargs)

    def _set_headers(self):
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

    def do_GET(self):
        res = {"error": "Path not found"}
        status = 404

        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        c = self.controller

        if self.path.startswith("/setmode"):
            status, res = onSetMode(c, params)

        if self.path.startswith("/enabled"):
            status, res = onEnabled(c, params)

        if self.path.startswith("/locked"):
            status, res = onLocked(c, params)

        if self.path.startswith("/speed"):
            status, res = onSetSpeed(c, params)

        if self.path.startswith("/filter"):
            status, res = onFilter(c, params)

        if self.path.startswith("/multiplier"):
            status, res = onMultiplier(c, params)

        if self.path.startswith("/energy"):
            status, res = onEnergy(c, params)

        if self.path.startswith("/vars"):
            status, res = onVars(c, params)

        if self.path.startswith("/available"):
            status, res = onAvailable(c, params)

        self.send_response(status)
        self._set_headers()
        self.wfile.write(json.dumps(res).encode("utf-8"))


class APIServer:
    def __init__(self, controller: "GeneralController"):
        self.controller = controller
        self.thread = None
        self.address = None
        self.port = None
        self.httpd = None

    def serve(self, address: str, port: int):
        if self.httpd is not None:
            print("HTTP Server already running. Returning")
            return

        httpd = ThreadedHTTPServer((address, port),
                                   lambda *_: APIServerHandler(self.controller, *_))

        print("Getting ips...")
        ips = getIPs()
        last_addr = ".".join(address.split(".")[:-1])

        if address == "0.0.0.0":
            matching_ips = ["127.0.0.1"]
            for ip in ips:
                if last_addr in ip:
                    matching_ips.append(ip)
        else:
            matching_ips = [address]

        print(f"API-Server[{self.controller.deviceId}] started listening on")
        for ip in matching_ips:
            print(f"    http://{ip}:{port}")

        self.address = address
        self.port = port
        self.httpd = httpd
        self.thread = Thread(target=httpd.serve_forever)
        self.thread.start()

    def shutdown(self):
        print(f"Shutting down API Server for {self.controller.deviceId}")
        self.httpd.shutdown()
        self.thread.join()
