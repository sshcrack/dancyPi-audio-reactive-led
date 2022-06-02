import config
import numpy as np
import base.visualization.dsp as dsp

gain = dsp.ExpFilter(np.tile(0.01, config.N_FFT_BINS),
                     alpha_decay=0.001, alpha_rise=0.99)


def getAvgEnergy(mel, pixels: int):
    """Effect that expands from the center with increasing sound energy"""
    mel = np.copy(mel)
    gain.update(mel)
    mel /= gain.value
    # Scale by the width of the LED strip
    mel *= float((pixels // 2) - 1)
    # Map color channels according to energy in the different freq bands
    scale = 0.9
    r = int(np.mean(mel[:len(mel) // 3] ** scale))
    g = int(np.mean(mel[len(mel) // 3: 2 * len(mel) // 3] ** scale))
    b = int(np.mean(mel[2 * len(mel) // 3:] ** scale))

    return min((r + g + b) / 3 / (pixels / 2) * 2, 2)
