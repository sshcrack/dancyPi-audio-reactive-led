import visualization.visualization as visualization
import config
import numpy as np


def full(mel):
    justWhite = [ ]
    for i in range(config.N_PIXELS):
        justWhite.append([ 255 ])

    return np.array([ justWhite, justWhite, justWhite ])


modes = {
    "scroll": {
        "func": visualization.visualize_scroll,
        "visualizer": True,
        "filters": True
    },
    "spectrum": {
        "func": visualization.visualize_spectrum,
        "visualizer": True,
        "filters": True
    },
    "energy": {
        "func": visualization.visualize_energy,
        "visualizer": True,
        "filters": True
    },
    "full": {
        "func": full,
        "visualizer": False,
        "filters": True
    },
}
modeKeys = modes.keys()
