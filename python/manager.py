from led.filters import applyFilters

import gesture.measure as gesture
import httpserver.server as server
import led.led as led
import visualization.microphone as microphone
import httpserver.currVars as currVars
import visualization.visualization as visualization
from modes import modes, modeKeys

print("Initizalizing Microphone...")
microphone.start()

print("Initializing HTTP server...")
server.start()

print("Loading config...")
currVars.load()
led.update()

def main():
    while True:
        mode = currVars.getMode()
        if not gesture.isEnabled():
            led.pixels *= 0
            led.update()
            continue

        if not mode in modeKeys:
            continue

        currMode = modes[mode]
        isVisualizer = currMode["visualizer"] or False
        useFilters = currMode["filters"] or False
        func = currMode["func"]

        funcOut = None
        micRunning = microphone.isRunning()
        if isVisualizer and not micRunning:
            microphone.start()

        if not isVisualizer and micRunning:
            microphone.stop()
        
        if isVisualizer:
            raw = microphone.read()
            mel = visualization.microphone_update(raw)
            funcOut = func(mel)
        else:
            funcOut = func()

        if useFilters:
            funcOut = applyFilters(funcOut);

        led.pixels = funcOut
        led.update()

try:
    main()
finally:
    print("Stopping microphone")
    microphone.stop()

    print("Stopping gesture")
    gesture.stop()

    print("Stopping led")
    led.stop()

    print("Saving config")
    currVars.save()