from http.server import BaseHTTPRequestHandler
from typing import  List

from httpserver.currVars import setConfig
from tools.tools import check_float, check_int
from httpserver.currVars import getAllVars


def onVars(_server: BaseHTTPRequestHandler, params: List[str]):
    return ( 200, getAllVars())