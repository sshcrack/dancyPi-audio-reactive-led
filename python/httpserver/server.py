from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from threading import Thread
from httpserver.setmode import onSetMode

def run_server():
    run(addr="0.0.0.0", port=6789)


class Server(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_header("Content-Type", "application/json")
        self.end_headers()

    def do_GET(self):
        res = { "error": "Path not found" }
        status = 404
        if self.path.startswith("/setmode"):
            setRes = onSetMode(self)

            status = setRes[0]
            res = setRes[1]

        self.send_response(status)
        self._set_headers()
        self.wfile.write(json.dumps(res).encode("utf-8"))

def run(server_class=HTTPServer, handler_class=Server, addr="localhost", port=8000):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)

    print(f"Starting httpd server on {addr}:{port}")
    httpd.serve_forever()

thread = Thread(target=run_server, daemon=True)

def start():
    if thread.is_alive():
        return

    thread.start()