from typing import List
from tools.tools import check_float
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from base.controller import GeneralController


def onSetSpeed(controller: "GeneralController", params: List[str]):
    speedRaw = params.get("speed")
    config = controller.config

    if speedRaw is not None and len(speedRaw) != 0:
        speedRaw: str = speedRaw[0]

    if not check_float(speedRaw):
        return (400,
                {
                    "error": f"Invalid speed {speedRaw}"
                })

    speed = float(speedRaw)
    config.setGeneralSpeed(speed)

    return (200, {
        "success": True,
        "speed": speed
    })
