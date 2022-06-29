import math

from base.controller import GeneralController
from base.modes.visualization import interpolate
from base.GeneralMode import GeneralMode
import numpy as np

from base.visualization import dsp
from tools.validators import validate_int


class ChunkMode(GeneralMode):
    def __init__(self, controller: GeneralController):
        dev = controller.device
        super().__init__({
            "chunk_chunks": 4
        }, {
            "visualizer": True,
            "filters": True,
            "required_vars": {
                "chunk_chunks": {
                    "sug_min": 1,
                    "sug_max": dev.N_PIXELS,
                    "func": validate_int("chunks", 1, dev.N_PIXELS),
                    "type": "int",
                    "min": 0
                }
            }
        }, controller)
        self._prev_spectrum = np.tile(0.01, dev.N_PIXELS // 2)
        self.common_mode = dsp.ExpFilter(np.tile(0.01, dev.N_PIXELS // 2),
                                         alpha_decay=0.99, alpha_rise=0.01)

        self.r_filt = dsp.ExpFilter(np.tile(0.01, dev.N_PIXELS // 2),
                                    alpha_decay=0.2, alpha_rise=0.99)
        self.b_filt = dsp.ExpFilter(np.tile(0.01, dev.N_PIXELS // 2),
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

        chunks = self.config.get("chunk_chunks")
        singleChunk = len(r) / chunks
        output = np.tile(1, (3, self.device.N_PIXELS))
        for i in range(chunks):
            startChunk = math.floor(singleChunk * i)
            endChunk = math.floor(singleChunk * (i + 1))

            rChunk = np.average(r[startChunk:endChunk]) * 255
            gChunk = np.average(g[startChunk:endChunk]) * 255
            bChunk = np.average(b[startChunk:endChunk]) * 255
            output[0][startChunk:endChunk] = rChunk
            output[1][startChunk:endChunk] = gChunk
            output[2][startChunk:endChunk] = bChunk

        return output