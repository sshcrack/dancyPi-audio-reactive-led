from socketserver import ThreadingMixIn
from http.server import HTTPServer


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """ This class allows handling requests in separated threads.
        No further content needed, don't touch this. """
