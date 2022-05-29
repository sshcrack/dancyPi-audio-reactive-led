from typing import List
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from base.controller import GeneralController


def onLocked(controller: "GeneralController", params: List[str]):
    locked_str = params.get("locked")
    
    if locked_str is not None and len(locked_str) != 0:
        locked_str = locked_str[0]

    config = controller.config
    if locked_str == "true":
        config.setLock(True)
    elif locked_str == "false":
        config.setLock(False)
    else:
        return (400, {
            "error": "Locked has to be either 'true' or 'false'"
        })

    locked = config.isLocked()
    return (200, {
        "result": f"Changed value to {locked}"
    })
