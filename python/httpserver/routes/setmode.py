from typing import List
from http.server import BaseHTTPRequestHandler
from data import modeKeys

from httpserver.currVars import setConfig, setMode
from tools.tools import check_float, isInt

def onSetMode(server: BaseHTTPRequestHandler, params: List[str]):
    mode = params.get("mode")
    concurrent = params.get("concurrent")
    speed = params.get("speed")

    shadow = params.get("shadow")
    size = params.get("size")

    if mode != None and len(mode) != 0:
        mode = mode[0]


    if concurrent != None and len(concurrent) != 0:
        concurrent = concurrent[0]

        
    if speed != None and len(speed) != 0:
        speed = speed[0]


    if shadow != None and len(shadow) != 0:
        shadow = shadow[0]

        
    if size != None and len(size) != 0:
        size = size[0]


    if mode not in modeKeys:
        return (400,
                {
                    "error": f"Invalid mode valid modes are {modeKeys}",
                    "mode": mode
                })

    if mode == "stack" :
        if concurrent == None or not isInt(concurrent):
            return (400,
                    {
                        "error": f"Invalid integer for concurrent {concurrent}",
                        "mode": mode
                    })

        concurrent_int = int(concurrent)
        if concurrent_int <= 0:
            return (400,
                    {
                        "error": f"Invalid integer for concurrent {concurrent} may no be zero or below",
                        "mode": mode
                    })


        if speed == None or not check_float(speed):
            return (400,
                    {
                        "error": f"Invalid float for speed {speed}",
                        "mode": mode
                    })

        speed_float = float(speed)
        setConfig("stack_concurrent", concurrent_int)
        setConfig("stack_speed", speed_float)

    if mode == "scanner" :
            if shadow == None or not isInt(shadow):
                return (400,
                        {
                            "error": f"Invalid integer for shadow {shadow}"
                        })

            shadow_int = int(shadow)
            if shadow_int <= 0:
                return (400,
                        {
                            "error": f"Invalid integer for shadow {shadow} may no be zero or below",
                            "mode": mode
                        })


            if size == None or not isInt(size):
                    return (400,
                            {
                                "error": f"Invalid integer for size {size}"
                            })

            size_int = int(size)
            if size_int <= 0:
                return (400,
                        {
                            "error": f"Invalid integer for size {size} may no be zero or below",
                            "mode": mode
                        })

            setConfig("scanner_shadow", shadow_int)
            setConfig("scanner_size", size_int)


    setMode(mode)
    return (200, {
        "success": True,
        "mode": mode
    })
