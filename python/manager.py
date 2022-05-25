import time

import config
import httpserver.server as server
import numpy as np
from data import applyFilters
from tools.energyspeed import getAvgEnergy
from tools.fps import frames_per_second
from tools.timer import setPrevTime
from tools.tools import getDeltaTime
import modes.visualization.microphone as microphone
import httpserver.currVars as currVars
import modes.visualization.visualization as visualization
from data import modes, modeKeys
import sys

gui_enabled = False
leds_available = False
gesture_available = False

try:
    import hardware.gesture.measure as gesture

    gesture_available = True
except BaseException as e:
    print(e)
    print("Could not find gesture sensor")

if "gui" in sys.argv:
    gui_enabled = True
    import gui.gui as gui

    gui.start()

try:
    import hardware.led.led as led

    leds_available = True
except BaseException as e:
    print("Could not import led module. ")
    print(e)
    if not gui_enabled:
        print("GUI not enabled, exiting...")
        sys.exit(-1)

print("Initializing Microphone...")
microphone.start()

print("Initializing HTTP server...")
server.start()

print("Loading config...")
currVars.load()

if leds_available:
    led.update()


def multipleIntArr(arr, numb, max_int=255, min_int=0):
    newArr = []
    for i in range(len(arr)):
        channel = arr[i]
        temp = []
        for x in range(len(channel)):
            maxMin = min(max(round(channel[x] * numb), min_int), max_int)
            temp.append(maxMin)
        newArr.append(temp)

    return np.array(newArr)


def getCurr():
    mode = currVars.getMode()

    if mode not in modeKeys:
        return [None, None, None]

    currMode = modes[mode]
    isVisualizer = currMode["visualizer"] or False
    useFilters = currMode["filters"] or False
    func = currMode["func"]

    return [isVisualizer, useFilters, func]


def micCheck(is_vis: bool):
    micRunning = microphone.isRunning()
    if is_vis and not micRunning:
        print("Starting microphone")
        microphone.start()

    if not is_vis and micRunning:
        print("Stopping microphone")
        microphone.stop()


def main():
    prev_fps_update = time.time()
    i = 0

    isVisualizer, useFilters, func = getCurr()
    isEnergySpeed = currVars.getConfig("energy_speed")
    isEnergyBrightness = currVars.getConfig("energy_brightness")
    energyBrightnessMult = currVars.getConfig("energy_brightness_mult")
    energySensitivity = currVars.getConfig("energy_sensitivity")

    micCheck(isVisualizer or isEnergyBrightness or isEnergySpeed)

    currEnabled = 1.0
    multiplier = currVars.getMultiplier()
    setPrevTime()
    while True:
        enabled = gesture.isEnabled() if gesture_available else currVars.getConfig("enabled")

        if not enabled and currEnabled == 0:
            led.pixels *= 0
            led.update()

            setPrevTime()
            continue
        if i > 50:
            isVisualizer, useFilters, func = getCurr()
            isEnergySpeed = currVars.getConfig("energy_speed")
            isEnergyBrightness = currVars.getConfig("energy_brightness")
            energyBrightnessMult = currVars.getConfig("energy_brightness_mult")
            micCheck(isVisualizer or isEnergyBrightness or isEnergySpeed)
            multiplier = currVars.getMultiplier()
            i = 0

        funcOut = None
        energy = None
        if isVisualizer or isEnergyBrightness or isEnergySpeed:
            raw = microphone.read()
            mel = visualization.microphone_update(raw)
            if isVisualizer:
                funcOut = func(mel)
                setPrevTime()
            else:
                energy = getAvgEnergy(mel) * energySensitivity
                currVars.setConfig("energy_curr", energy)

        if not isVisualizer:
            funcOut = func()
            setPrevTime()

        if useFilters:
            funcOut = applyFilters(funcOut)
            if energy is not None and isEnergyBrightness:
                funcOut = multipleIntArr(funcOut, energy * energyBrightnessMult)

        delta = getDeltaTime()
        if enabled and currEnabled < 1:
            funcOut = multipleIntArr(funcOut, currEnabled)
            currEnabled = min(currEnabled + delta * 8, 1)
        elif not enabled and currEnabled > 0:
            funcOut = multipleIntArr(funcOut, currEnabled)
            currEnabled = max(0, currEnabled - delta * 3)
        else:
            if multiplier != 1:
                funcOut *= multipleIntArr(funcOut, multiplier)

        if leds_available:
            led.pixels = funcOut
            led.update()
        if gui_enabled:
            gui.update(funcOut)
            if gui.exitSignal:
                raise Exception("Exit by GUI")
        i += 1

        if config.DISPLAY_FPS:
            fps = frames_per_second()
            if time.time() - 0.5 > prev_fps_update:
                prev_fps_update = time.time()
                print('FPS {:.0f} / {:.0f}'.format(fps, config.FPS))


try:
    main()
finally:
    print("Saving config")
    currVars.save()

    print("Stopping microphone")
    microphone.stop()

    if gesture_available:
        print("Stopping gesture")
        gesture.stop()

    if leds_available:
        print("Stopping led")
        led.stop()

    if gui_enabled:
        print("Stopping gui...")
        gui.stop()

    print("Cleaning up GPIO...")
    currVars.cleanupGPIO()
