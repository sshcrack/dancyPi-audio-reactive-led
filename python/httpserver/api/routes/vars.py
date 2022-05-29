from http.server import BaseHTTPRequestHandler
from typing import List
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from base.controller import GeneralController


def onVars(controller: "GeneralController", params: List[str]):
    return 200, controller.config.getAll()
