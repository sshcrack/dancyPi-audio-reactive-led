import filters.rainbow
import filters.normal
import filters.hex
import modes.visualization.visualization as visualization
import modes.full
import modes.stack
import modes.scanner

from httpserver.currVars import getFilterMode


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
        "func": modes.full.full,
        "visualizer": False,
        "filters": True
    },
    "stack": {
        "func": modes.stack.stack,
        "visualizer": False,
        "filters": True
    },
    "scanner": {
        "func": modes.scanner.scanner,
        "visualizer": False,
        "filters": True
    },
}
modeKeys = modes.keys()


rgb_index = 0


filters = {
    "hex": filters.hex.hex,
    "rainbow": filters.rainbow.rainbow,
    "normal": filters.normal.normal
}

def applyFilters(data):
    filter_mode = getFilterMode()
    filter = filters[filter_mode]

    return filter(data)
