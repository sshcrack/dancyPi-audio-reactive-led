import config
import filters.rainbow
import filters.normal
import filters.hex
import modes.visualization.visualization as visualization
import modes.visualization.chunk as chunk
import modes.full
import modes.stack
import modes.scanner

from tools.validators import validate_float, validate_int, validate_bool
from httpserver.currVars import getFilterMode

required_parsable = ["min", "max", "type", "sug_min", "sug_max"]

# ! Make sure that required vars are prefixed with root key (REQUIRED)
modes = {
    "scroll": {
        "func": visualization.visualize_scroll,
        "visualizer": True,
        "filters": True,
        "required_vars": {}
    },
    "spectrum": {
        "func": visualization.visualize_spectrum,
        "visualizer": True,
        "filters": True,
        "required_vars": {}
    },
    "energy": {
        "func": visualization.visualize_energy,
        "visualizer": True,
        "filters": True,
        "required_vars": {
            "energy_mirror": {
                "type": "boolean",
                "func": validate_bool("mirror")
            }
        }
    },
    "full": {
        "func": modes.full.full,
        "visualizer": False,
        "filters": True,
        "required_vars": {}
    },
    "stack": {
        "func": modes.stack.stack,
        "visualizer": False,
        "filters": True,
        "required_vars": {
            "stack_concurrent": {
                "sug_max": 30,
                "sug_min": 1,
                "func": validate_int("concurrent", 1),
                "type": "int",
                "min": 1
            },
            "stack_speed": {
                "sug_max": 15,
                "sug_min": 0,
                "min": 0,
                "func": validate_float("speed"),
                "type": "float"
            }
        }
    },
    "scanner": {
        "func": modes.scanner.scanner,
        "visualizer": False,
        "filters": True,
        "required_vars": {
            "scanner_shadow": {
                "sug_min": 0,
                "sug_max": 100,
                "func": validate_int("shadow", 0),
                "type": "int",
                "min": 0
            },
            "scanner_size": {
                "func": validate_int("size", 1),
                "type": "int",
                "sug_min": 1,
                "sug_max": 30,
                "min": 1
            }
        }
    },
    "chunk": {
        "func": chunk.chunk,
        "visualizer": True,
        "filters": True,
        "required_vars": {
            "chunk_chunks": {
                "sug_min": 1,
                "sug_max": config.N_PIXELS,
                "func": validate_int("chunks", 1, config.N_PIXELS),
                "type": "int",
                "min": 0
            }
        }
    },
}
modeKeys = modes.keys()

rgb_index = 0

filters = {
    "hex": {
        "func": filters.hex.hex,
        "required_vars": {
            "hex_gradient": {
                "func": filters.hex.validateGradient,
                "type": "gradient"
            }
        }
    },
    "rainbow": {
        "func": filters.rainbow.rainbow,
        "required_vars": {
            "rainbow_speed": {
                "func": validate_float("speed"),
                "type": "float",
                "sug_min": 0,
                "sug_max": 1250
            }
        }
    },
    "normal": {
        "func": filters.normal.normal,
        "required_vars": {}
    }
}


def applyFilters(data):
    filter_mode = getFilterMode()
    curr_filter = filters[filter_mode]["func"]

    return curr_filter(data)
