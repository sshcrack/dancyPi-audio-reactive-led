from base.GeneralPostProcess import GeneralPostProcess
from typing import Any, Dict, Optional
import base.visualization.dsp as dsp
import config
import numpy as np
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from base.controller import GeneralController


class VisualizerMode(GeneralPostProcess):
    def __init__(self, configDefaults: Dict[str, Any], modeData: Dict[str, Any], controller: "GeneralController"):
        super().__init__(configDefaults, modeData, controller)

        self.p_filt = dsp.ExpFilter(np.tile(1, (3, self.device.N_PIXELS // 2)),
                                    alpha_decay=0.1, alpha_rise=0.99)
        self.p = np.tile(1.0, (3, self.device.N_PIXELS // 2))
        self.gain = dsp.ExpFilter(np.tile(0.01, config.N_FFT_BINS),
                                  alpha_decay=0.001, alpha_rise=0.99)

    def run(self, mel: Optional[Any]):
        raise NotImplementedError
