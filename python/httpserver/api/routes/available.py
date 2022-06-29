from __future__ import annotations

from typing import List
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from base.controller import GeneralController
from httpserver.httpTypings import required_parsable


def onAvailable(controller: "GeneralController", params: List[str]):
    allFilters = dataToJSONDumpable("filters", controller.filters)
    allModes = dataToJSONDumpable("modes", controller.modes)

    return (200, {
        "filters": allFilters,
        "modes": allModes
    })


def dataToJSONDumpable(name: str, data):
    total = []

    keys = list(data.keys())
    for effect_key in keys:
        vars_json = []
        effect = data[effect_key]

        required_vars = effect.data["required_vars"]
        required_vars_keys = list(required_vars.keys())
        for key in required_vars_keys:
            el = required_vars[key]
            el_keys = list(el.keys())

            to_add = {}

            for curr in required_parsable:
                if curr in el_keys:
                    to_add[curr] = el[curr]

            vars_json.append({
                **to_add,
                "name": key.replace(f"{effect_key}_", "")
            })

        total.append({
            "name": effect_key,
            "vars": vars_json
        })

    return total
