from typing import Any, Optional
from base.GeneralPostProcess import GeneralPostProcess


class GeneralMode(GeneralPostProcess):
    def run(self, mel: Optional[Any]):
        raise NotImplementedError
