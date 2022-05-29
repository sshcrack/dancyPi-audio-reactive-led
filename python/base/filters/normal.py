from base.GeneralMode import GeneralMode
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from base.controller import GeneralController


class NormalMode(GeneralMode):
    def __init__(self, controller: "GeneralController"):
        super().__init__({}, {
            "required_vars": {}
        }, controller)

    def run(self, data):
        return data
