from typing import  TypeVar
import re
import time


def timeit(func):
    """
    Decorator for measuring function's running time.
    """
    def measure_time(*args, **kw):
        start_time = time.time()
        result = func(*args, **kw)
        print("Processing time of %s(): %.2f seconds."
              % (func.__qualname__, time.time() - start_time))
        return result

    return measure_time


def rgb_to_hex(r, g, b):
    return f'#{r << 16 | g << 8 | b:06x}'


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


def check_int(potential_int: str):
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
    except TypeError:
        return False


def checkInt(potential_int):
    try:
        int(potential_int)
        return True
    except ValueError:
        return False
    except TypeError:
        return False


def check_bool(potential_bool: str):
    return potential_bool.lower() == "true" or potential_bool.lower() == "false"


def isColorHex(s: str):
    return re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', str(s))


T = TypeVar("T")


def clamp(min_numb: T, value: T, max_numb: T):
    if value < min_numb:
        return min_numb
    if value > max_numb:
        return max_numb

    return value
