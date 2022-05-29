from typing import Any, Dict, Optional
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from base.controller import GeneralController


class GeneralPostProcess:
    def __init__(self, configDefaults: Dict[str, Any], modeData: Dict[str, Any], controller: "GeneralController"):
        self.configDefaults = configDefaults
        self.controller = controller
        self.config = controller.config
        self.device = controller.device
        self.timer = controller.timer
        self.data = modeData

    def run(self, mel: Optional[Any]):
        raise NotImplementedError("Function has to be implemented.")
