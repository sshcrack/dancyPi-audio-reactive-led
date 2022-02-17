from http.server import BaseHTTPRequestHandler
from typing import  List

from data import required_parsable, filters, modes


def onAvailable(_server: BaseHTTPRequestHandler, params: List[str]):
    allFilters = dataToJSONDumpable("filters", filters)
    allModes = dataToJSONDumpable("modes", modes)


    return ( 200, {
        "filters": allFilters,
        "modes": allModes
    })

def dataToJSONDumpable(name: str, data):
    total = []

    keys = list(data.keys())
    for effect_key in keys:
        vars_json = []
        effect = data[effect_key]

        required_vars = effect["required_vars"]
        required_vars_keys = list(required_vars.keys())
        for key in required_vars_keys:
            el = required_vars[key]
            el_keys = list(el.keys())

            to_add = { }

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
