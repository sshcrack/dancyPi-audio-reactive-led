from scipy.ndimage import gaussian_filter1d

import numpy as np
from base.modes.visualizerMode import VisualizerMode
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from base.controller import GeneralController


class ScrollVisualizerMode(VisualizerMode):
    def __init__(self, controller: "GeneralController"):
        super().__init__({}, {
            "visualizer": True,
            "filters": True,
            "required_vars": {}
        }, controller)

    def run(self, mel):
        """Effect that originates in the center and scrolls outwards"""
        mel = mel ** 2.0
        self.gain.update(mel)
        mel /= self.gain.value
        mel *= 255.0
        r = int(np.max(mel[:len(mel) // 3]))
        g = int(np.max(mel[len(mel) // 3: 2 * len(mel) // 3]))
        b = int(np.max(mel[2 * len(mel) // 3:]))
        # Scrolling effect window
        self.p[:, 1:] = self.p[:, :-1]
        self.p *= 0.98
        self.p = gaussian_filter1d(self.p, sigma=0.2)
        # Create new color originating at the center
        self.p[0, 0] = r
        self.p[1, 0] = g
        self.p[2, 0] = b
        # Update the LED strip
        return np.concatenate((self.p[:, ::-1], self.p), axis=1)