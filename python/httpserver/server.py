from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
import json
from os import path
from socketserver import ThreadingMixIn
from threading import Thread
from urllib.parse import parse_qs, urlparse
from httpserver.routes.available import onAvailable
from httpserver.routes.enabled import onEnabled
from httpserver.routes.energy import onEnergy
from httpserver.routes.multiplier import onMultiplier
from httpserver.routes.setmode import onSetMode
from httpserver.routes.filter import onFilter
from httpserver.routes.setspeed import onSetSpeed
from httpserver.routes.vars import onVars
import mimetypes

from interfaces import getIPs

def run_server():
    run(addr="0.0.0.0", port=6789)

websiteFiles = path.join(path.dirname(path.realpath(__file__)), "../..", "website", "build")
class Handler(BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

    def do_GET(self):
        res = { "error": "Path not found" }
        status = 404

        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
    
        if self.path.startswith("/setmode"):
            status, res = onSetMode(self, params)
            
        if self.path.startswith("/enabled"):
            status, res = onEnabled(self, params)

        if self.path.startswith("/speed"):
            status, res = onSetSpeed(self, params)


        if self.path.startswith("/filter"):
            status, res = onFilter(self, params)

        if self.path.startswith("/multiplier"):
            status, res = onMultiplier(self, params)
            
        if self.path.startswith("/energy"):
            status, res = onEnergy(self, params)

        if self.path.startswith("/vars"):
            status, res = onVars(self, params)

        if self.path.startswith("/available"):
            status, res = onAvailable(self, params)

        if status == 404:
            return self.serveStaticFiles()

        self.send_response(status)
        self._set_headers()
        self.wfile.write(json.dumps(res).encode("utf-8"))

    
    def serveStaticFiles(self):
        server_path = self.path.replace("..", "")[1:]
        first_lookup = path.join(websiteFiles, server_path)

        def defaultReturn(file_path: str):
            mime = "text/plain"
            guessed = mimetypes.guess_type(file_path)
            if guessed:
                mime = guessed[0]
            
            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Type", mime)
            self.end_headers()

            with open(file_path, "rb") as file:
                self.wfile.write(file.read())

        if path.isfile(first_lookup):
            return defaultReturn(first_lookup)

        index_file = path.join(websiteFiles, server_path, "index.html")
        
        if path.isfile(index_file):
            return defaultReturn(index_file)
        
        self.send_response(404)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Type", "text/plain")
        self.end_headers()

        self.wfile.close()
        return

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """ This class allows to handle requests in separated threads.
        No further content needed, don't touch this. """


def run(server_class=ThreadedHTTPServer, handler_class=Handler, addr="localhost", port=8000):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)


    ips = [addr]
    if addr == "0.0.0.0":
        ips = getIPs()
    
    print("Server started listening on")
    for ip in ips:
        print(f"    http://{ip}:{port}")

    httpd.serve_forever()

thread = Thread(target=run_server, daemon=True)

def start():
    if thread.is_alive():
        return

    thread.start()
