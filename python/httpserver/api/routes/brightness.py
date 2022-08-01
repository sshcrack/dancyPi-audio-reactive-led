from typing import List
from typing import TYPE_CHECKING

from tools.validators import validate_float

if TYPE_CHECKING:
    from base.controller import GeneralController

validateFunc = validate_float("brightness", 0, 100)


def onBrightness(controller: "GeneralController", params: List[str]):
    brightness_str = params.get("brightness")

    config = controller.config
    validated = validateFunc(brightness_str)
    if validated.get("result") is None:
        return 400, validated

    res = validated.get("result")
    print("Setting brightness to", res)
    config.set("brightness", res)
    return (200, {
        "result": f"Changed brightness to {res}"
    })
