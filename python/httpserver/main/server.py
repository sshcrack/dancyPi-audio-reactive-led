from http.server import BaseHTTPRequestHandler
import json
from typing import Dict
import re

from os import path
from threading import Thread
from urllib.parse import parse_qs, urlparse
import mimetypes

from httpserver.base import ThreadedHTTPServer
from httpserver.main.routes.allenabled import onAllEnabled
from httpserver.main.routes.devices_list import onDevicesList
from httpserver.main.routes.devices_options import onDevicesOptions
from tools.interfaces import getIPs
from httpserver.api.apiServer import AVAILABLE_ROUTES
from typing import TYPE_CHECKING
import requests

if TYPE_CHECKING:
    from base.controller import GeneralController

websiteFiles = path.join(path.dirname(path.realpath(__file__)), "../../..", "website", "build")


class MainHTTPServerHandler(BaseHTTPRequestHandler):
    def __init__(self, controllers: Dict[str, "GeneralController"], *args, **kwargs):
        self.controllers = controllers
        super().__init__(*args, **kwargs)

    def _set_headers(self):
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)

        deviceId = params.get("device_id")
        for apiRoutes in AVAILABLE_ROUTES:
            if self.path.startswith(f"/{apiRoutes}"):
                if deviceId is None or len(deviceId) == 0 or deviceId[0] is None:
                    print(f"Invalid request, no device id")
                    self.send_response(401)
                    self._set_headers()
                    self.wfile.write(
                        '{"error": "device_id has to be in parameters to use api functions and has to be a string"}'.encode(
                            "utf-8"))
                    return
                c = self.controllers.get(deviceId[0])
                if c is None:
                    print(f"No controller could be found for {deviceId[0]}")
                    self.send_response(401)
                    self._set_headers()
                    self.wfile.write(json.dumps({
                        "error": "Controller could not be found",
                        "available": list(self.controllers.keys())
                    }).encode("utf-8"))
                    return
                server = c.api
                address = server.address
                port = server.port

                raw_path = re.sub("[^0-9a-zA-Z]+", "", parsed.path)
                url = f"http://{address}:{port}/{raw_path}?{parsed.query}"
                print(f"Requesting url {url}")
                resp = requests.get(url)
                body = resp.text
                headers = resp.headers
                print("Writing response")
                self.send_response(resp.status_code)
                for key in list(headers.keys()):
                    self.send_header(key, headers[key])
                self.end_headers()
                self.wfile.write(body.encode("utf-8"))
                return

        status, res = (404, {"error": "Path not found"})
        p = parsed.path
        if p == "/devices/list":
            print("deivces list")
            status, res = onDevicesList(self.controllers, params)
        if p == "/devices/options":
            print("Device options")
            status, res = onDevicesOptions(self.controllers, params)
        if p == "/allenabled":
            status, res = onAllEnabled(self.controllers, params)

        if status == 404:
            print("Serving static file")
            return self.serveStaticFiles(p)

        self.send_response(status)
        self._set_headers()
        self.wfile.write(json.dumps(res).encode("utf-8"))

    def serveStaticFiles(self, req_path: str):
        server_path = req_path.replace("..", "")[1:]
        first_lookup = path.join(websiteFiles, server_path)
        print(server_path)

        def defaultReturn(file_path: str):
            mime = "text/plain"
            guessed = mimetypes.guess_type(file_path)
            if guessed:
                mime = guessed[0]

            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Type", mime)
            self.end_headers()

            print("Reading file", file_path)
            with open(file_path, "rb") as file:
                self.wfile.write(file.read())

        if path.isfile(first_lookup):
            return defaultReturn(first_lookup)

        index_file = path.join(websiteFiles, server_path, "index.html")

        if path.isfile(index_file):
            return defaultReturn(index_file)

        self.send_response(404)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Type", "text/html")
        self.end_headers()

        self.wfile.write("<h1>404 Not Found</h1>".encode("utf-8"))
        return


class MainHTTPServer:
    def __init__(self, controllers: Dict[str, "GeneralController"]):
        self.controllers = controllers
        self.thread = None
        self.address = None
        self.port = None
        self.httpd = None

    def serve(self, address: str, port: int):
        if self.httpd is not None:
            print("HTTP Server already running. Returning")
            return

        httpd = ThreadedHTTPServer((address, port),
                                   lambda *_: MainHTTPServerHandler(self.controllers, *_))

        print("Getting ips...")
        ips = getIPs()

        if address == "0.0.0.0":
            matching_ips = ["127.0.0.1"]
            for ip in ips:
                matching_ips.append(ip)
        else:
            matching_ips = [address]

        print(f"Main Server started listening on")
        for ip in matching_ips:
            print(f"    http://{ip}:{port}")

        self.address = address
        self.port = port
        self.httpd = httpd
        self.thread = Thread(target=httpd.serve_forever, name="MAIN_SERVER")
        self.thread.start()

    def shutdown(self):
        print(f"Shutting down Main Server")
        self.httpd.shutdown()
        self.thread.join()
