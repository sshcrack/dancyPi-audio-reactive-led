import numpy as np
from base.GeneralPostProcess import GeneralPostProcess
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from base.controller import GeneralController


class FullMode(GeneralPostProcess):
    def __init__(self, controller: "GeneralController"):
        super().__init__({}, {
            "visualizer": False,
            "filters": True,
            "required_vars": {}
        }, controller)

    def run(self, mel):
        justWhite = []
        dev = self.controller.device
        for _ in range(dev.N_PIXELS):
            justWhite.append(255)

        return np.array([justWhite, justWhite, justWhite])
