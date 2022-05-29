import numpy as np

from base.modes.visualization import interpolate
from base.modes.visualizerMode import VisualizerMode
import base.visualization.dsp as dsp
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from base.controller import GeneralController


class SpectrumVisualizerMode(VisualizerMode):
    def __init__(self, controller: "GeneralController"):
        super().__init__({}, {
            "visualizer": True,
            "filters": True,
            "required_vars": {}
        }, controller)
        self._prev_spectrum = np.tile(0.01, self.device.N_PIXELS // 2)
        self.common_mode = dsp.ExpFilter(np.tile(0.01, self.device.N_PIXELS // 2),
                                         alpha_decay=0.99, alpha_rise=0.01)

        self.r_filt = dsp.ExpFilter(np.tile(0.01, self.device.N_PIXELS // 2),
                                    alpha_decay=0.2, alpha_rise=0.99)
        self.g_filt = dsp.ExpFilter(np.tile(0.01, self.device.N_PIXELS // 2),
                                    alpha_decay=0.05, alpha_rise=0.3)
        self.b_filt = dsp.ExpFilter(np.tile(0.01, self.device.N_PIXELS // 2),
                                    alpha_decay=0.1, alpha_rise=0.5)

    def run(self, mel):
        mel = np.copy(interpolate(mel, self.device.N_PIXELS // 2))
        self.common_mode.update(mel)
        diff = mel - self._prev_spectrum
        _prev_spectrum = np.copy(mel)
        # Color channel mappings
        r = self.r_filt.update(mel - self.common_mode.value)
        g = np.abs(diff)
        b = self.b_filt.update(np.copy(mel))
        # Mirror the color channels for symmetric output
        r = np.concatenate((r[::-1], r))
        g = np.concatenate((g[::-1], g))
        b = np.concatenate((b[::-1], b))

        output = np.array([r, g, b]) * 255
        return output
