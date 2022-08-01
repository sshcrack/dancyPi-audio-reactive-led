from scipy.ndimage import gaussian_filter1d

import numpy as np
from base.modes.visualizerMode import VisualizerMode
from tools.validators import validate_bool
from base.modes.visualization import interpolate
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from base.controller import GeneralController


class EnergyVisualizerMode(VisualizerMode):
    def __init__(self, controller: "GeneralController"):
        super().__init__({
            "energy_mirror": True
        }, {
            "visualizer": True,
            "filters": True,
            "required_vars": {
                "energy_mirror": {
                    "type": "boolean",
                    "func": validate_bool("mirror")
                }
            }
        }, controller)

    def run(self, mel):
        mirror = self.config.get("energy_mirror", True)

        mel = np.copy(mel)
        self.gain.update(mel)
        mel /= self.gain.value
        # Scale by the width of the LED strip
        mel *= float((self.device.N_PIXELS // 2) - 1)
        # Map color channels according to energy in the different freq bands
        scale = 0.9
        r = int(np.mean(mel[:len(mel) // 3] ** scale))
        g = int(np.mean(mel[len(mel) // 3: 2 * len(mel) // 3] ** scale))
        b = int(np.mean(mel[2 * len(mel) // 3:] ** scale))
        # Assign color to different frequency regions
        self.p[0, :r] = 255.0
        self.p[0, r:] = 0.0
        self.p[1, :g] = 255.0
        self.p[1, g:] = 0.0
        self.p[2, :b] = 255.0
        self.p[2, b:] = 0.0
        self.p_filt.update(self.p)
        self.p = np.round(self.p_filt.value)
        # Apply substantial blur to smooth the edges
        self.p[0, :] = gaussian_filter1d(self.p[0, :], sigma=4.0)
        self.p[1, :] = gaussian_filter1d(self.p[1, :], sigma=4.0)
        self.p[2, :] = gaussian_filter1d(self.p[2, :], sigma=4.0)

        N_PIXELS = self.device.N_PIXELS
        if mirror:
            return np.concatenate((self.p[:, ::-1], self.p), axis=1)
        else:
            r_l = interpolate(self.p[0], N_PIXELS)
            g_l = interpolate(self.p[1], N_PIXELS)
            b_l = interpolate(self.p[2], N_PIXELS)
            return np.array([r_l, g_l, b_l])
