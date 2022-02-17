from http.server import BaseHTTPRequestHandler
import json
from typing import Any, List
from data import filters

import re

from httpserver.currVars import setConfig, setFilterMode, setGradient

availableModes = list(filters.keys())
def onFilter(_server: BaseHTTPRequestHandler, params: List[str]):
    filter_str = params.get("mode")

    if filter_str != None and len(filter_str) != 0:
        filter_str = filter_str[0]

    if filter_str not in availableModes:
        return (400,
                {
                    "error": f"Invalid mode valid modes are {availableModes}"
                })

    curr_filter = filters[filter_str]
    required_vars = curr_filter["required_vars"]
    
    if type(required_vars) is dict:
        usual_prefix = f"{filter_str}_"

        for key in required_vars.keys():
            param_key = key
            if key.startswith(usual_prefix):
                param_key = param_key.replace(usual_prefix, "")

            func = required_vars[key]["func"]
            res = func(params.get(param_key))
            res_keys = res.keys()

            if "error" in res_keys:
                return (400,
                {
                    "error": res["error"]
                })

            if "result" not in res_keys:
                return (500,
                {
                    "error": f"Validate function filter {filter_str} with key {key} did not return any value"
                })
            
            setConfig(key, res["result"])
    setFilterMode(filter_str)

    return (200, {
        "success": True,
        "mode": filter_str
    })