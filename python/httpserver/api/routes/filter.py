from typing import List
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from base.controller import GeneralController


def onFilter(controller: "GeneralController", params: List[str]):
    filter_str = params.get("mode")
    filters = controller.filters
    availableFilters = list(filters.keys())
    config = controller.config

    if filter_str is not None and len(filter_str) != 0:
        filter_str = filter_str[0]

    if filter_str not in availableFilters:
        return (400,
                {
                    "error": f"Invalid mode valid modes are {availableFilters}"
                })

    curr_filter = filters[filter_str]
    required_vars = curr_filter.data["required_vars"]
    
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
            
            config.set(key, res["result"])
            print("Setting", key, "to", res["result"])
            config.set("filter_mode", filter_str)

    return (200, {
        "success": True,
        "mode": filter_str
    })