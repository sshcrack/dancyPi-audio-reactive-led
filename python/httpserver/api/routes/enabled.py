from typing import List
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from base.controller import GeneralController


def onEnabled(controller: "GeneralController", params: List[str]):
    enabled_str = params.get("enabled")

    config = controller.config
    if enabled_str is not None and len(enabled_str) != 0:
        enabled_str = enabled_str[0]

    if enabled_str == "true":
        config.set("enabled", True)
    elif enabled_str == "false":
        config.set("enabled", False)
    else:
        return (400, {
            "error": "Enabled has to be either 'true' or 'false'"
        })

    enabled = config.get("enabled")
    return (200, {
        "result": f"Changed value to {enabled}"
    })
