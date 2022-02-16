from time import time
import config
import numpy as np
from typing import Optional
import modes.visualization.dsp as dsp

from tools.timer import getPrevTime


def hex_to_rgb(hex_string):
    r_hex = hex_string[1:3]
    g_hex = hex_string[3:5]
    b_hex = hex_string[5:7]
    return int(r_hex, 16), int(g_hex, 16), int(b_hex, 16)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    pos = pos % 255
    if pos < 85:
        return [pos * 3, 255 - pos * 3, 0]
    elif pos < 170:
        pos -= 85
        return [255 - pos * 3, 0, pos * 3]
    else:
        pos -= 170
        return [0, pos * 3, 255 - pos * 3]

def getDeltaTime(currTime: Optional[float]=None):
    _time_prev = getPrevTime()
    if currTime == None:
        currTime = time()

    return (currTime - _time_prev)
    

    
def isInt(potential_int: str):
    try:
        int(potential_int)
        return True
    except ValueError:

        return False

        
def check_float(potential_float):
    try:
        float(potential_float)
        return True
    except ValueError:

        return False


gain = dsp.ExpFilter(np.tile(0.01, config.N_FFT_BINS),
                     alpha_decay=0.01, alpha_rise=0.99)

def getAvgEnergy(mel):
    """Effect that expands from the center with increasing sound energy"""
    global p
    mel = np.copy(mel)
    gain.update(mel)
    mel /= gain.value
    # Scale by the width of the LED strip
    mel *= float((config.N_PIXELS // 2) - 1)
    # Map color channels according to energy in the different freq bands
    scale = 0.9
    r = int(np.mean(mel[:len(mel) // 3]**scale))
    g = int(np.mean(mel[len(mel) // 3: 2 * len(mel) // 3]**scale))
    b = int(np.mean(mel[2 * len(mel) // 3:]**scale))

    return min((r + g + b) / 3 / (config.N_PIXELS / 2) * 2, 2)