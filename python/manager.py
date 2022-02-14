import sys

import gesture.measure as gesture
import httpserver.server as server
import led
import microphone
import visualization
from httpserver.currVars import getMode

print("Initizalizing Microphone...")
microphone.start()

print("Initializing...")
server.start()

led.update()

visualizers = {
    "scroll": visualization.visualize_scroll,
    "spectrum": visualization.visualize_spectrum,
    "energy": visualization.visualize_energy
}
visualizer_keys = visualizers.keys()

def main():
    while True:
        mode = getMode()

        if not gesture.isEnabled():
            led.pixels *= 0
            led.update()

        if mode in visualizer_keys:
            val = microphone.read()
            if len(val) != 0:
                led.pixels = visualizers[mode](val)
            else:
                led.pixels *= 0
            
            led.update()

try:
    main()
except Exception as err:
    print(f"Error {err}")

    print("Stopping microphone")
    microphone.stop()

    print("Stopping gesture")
    gesture.stop()

    print("Stopping led")
    led.stop()
    raise(err)
