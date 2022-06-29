from typing import List

from tools.tools import check_float
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from base.controller import GeneralController


def onEnergy(controller: "GeneralController", params: List[str]):
    bright_bool = params.get("brightness")
    speed_bool = params.get("speed")
    sensitivity_str = params.get("sensitivity")
    speed_mult_str = params.get("speed_mult")
    brightness_mult_str = params.get("brightness_mult")

    if bright_bool is not None and len(bright_bool) != 0:
        bright_bool = bright_bool[0]

    if speed_bool is not None and len(speed_bool) != 0:
        speed_bool = speed_bool[0]

    if sensitivity_str is not None and len(sensitivity_str) != 0:
        sensitivity_str = sensitivity_str[0]

    if speed_mult_str is not None and len(speed_mult_str) != 0:
        speed_mult_str = speed_mult_str[0]

    if brightness_mult_str is not None and len(brightness_mult_str) != 0:
        brightness_mult_str = brightness_mult_str[0]

    if bright_bool == "true":
        bright_res = True
    elif bright_bool == "false":
        bright_res = False
    else:
        return (400, {
            "error": "Brightness can either be 'true' or 'false'"
        })

    if speed_bool == "true":
        speed_res = True
    elif speed_bool == "false":
        speed_res = False
    else:
        return (400, {
            "error": "Speed can either be 'true' or 'false'"
        })

    if not check_float(sensitivity_str):
        return (400, {
            "error": f"Sensitivity can not be {sensitivity_str} (not valid float)"
        })

    if not check_float(brightness_mult_str):
        return (400, {
            "error": f"brightness_mult can not be {brightness_mult_str} (not valid float)"
        })

    if not check_float(speed_mult_str):
        return (400, {
            "error": f"speed_mult can not be {speed_mult_str} (not valid float)"
        })

    sense = float(sensitivity_str)
    if sense > .99 or sense < 0:
        return (400, {
            "error": "Sensitivity has to be below .99 and equal or above 0"
        })

    config = controller.config
    config.set("energy_brightness", bright_res)
    config.set("energy_brightness_mult", float(brightness_mult_str))
    config.set("energy_speed", speed_res)
    config.set("energy_speed_mult", float(speed_mult_str))
    config.set("energy_sensitivity", sense)

    return (200, {
        "success": True
    })
