from typing import List
from typing import TYPE_CHECKING
from tools.tools import check_float

if TYPE_CHECKING:
    from base.controller import GeneralController


def onMultiplier(controller: "GeneralController", params: List[str]):
    multiplierRaw = params.get("multiplier")

    if multiplierRaw is not None and len(multiplierRaw) != 0:
        multiplierRaw: str = multiplierRaw[0]

    if not check_float(multiplierRaw):
        return (400,
                {
                    "error": f"Invalid multiplier {multiplierRaw}"
                })

    multiplier = float(multiplierRaw)
    controller.config.set("multiplier", multiplier)

    return (200, {
        "success": True,
        "speed": multiplier
    })
