from tools.tools import check_float, check_int


def validate_int(param_name: str, min_val = None, max_val = None):
    def func(param):
        if param == None or len(param) == 0 or param[0] == None:
            return {
                "error": f"{param_name} has to have an value",
                "result": None
            }

        param = param[0]
        if not check_int(param):
            return {
                "error": f"{param_name} has to be an integer",
                "result": None
            }
        
        res = int(param)
        if (min_val != None and res < min_val) or (max_val != None and res > max_val):
            return {
                "error": f"{param_name} can not be below {min_val} and not above {max_val}",
                "result": None
            }

        return {
            "result": res
        }

    return func


def validate_float(param_name: str, min_val = None, max_val = None):
    def func(param):
        if param == None or len(param) == 0 or param[0] == None:
            return {
                "error": f"{param_name} has to have an value",
                "result": None
            }

        param = param[0]
        if not check_float(param):
            return {
                "error": f"{param_name} has to be a float",
                "result": None
            }
        
        res = float(param)
        if (min_val != None and res < min_val) or (max_val != None and res > max_val):
            return {
                "error": f"{param_name} can not be below {min_val} and not above {max_val}",
                "result": None
            }

        return {
            "result": res
        }

    return func