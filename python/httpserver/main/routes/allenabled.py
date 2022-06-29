from typing import Dict, TYPE_CHECKING, List

if TYPE_CHECKING:
    from base.controller import GeneralController


def onAllEnabled(controllers: Dict[str, "GeneralController"], params: List[str]):
    enabled_str = params.get("enabled")

    if enabled_str is not None and len(enabled_str) != 0:
        enabled_str = enabled_str[0]

    if enabled_str == "true":
        enabled = True
    elif enabled_str == "false":
        enabled = False
    else:
        return (400, {
            "error": "Enabled has to be either 'true' or 'false'"
        })

    for c in controllers.values():
        c.config.set("enabled", enabled)

    return 200, { "enabled": enabled }
