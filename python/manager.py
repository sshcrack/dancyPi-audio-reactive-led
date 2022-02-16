import math
import config

import hardware.gesture.measure as gesture
import httpserver.server as server
import hardware.led.led as led
import numpy as np
from data import applyFilters
from tools.timer import setPrevTime
from tools.tools import getAvgEnergy, getDeltaTime
import modes.visualization.microphone as microphone
import httpserver.currVars as currVars
import modes.visualization.visualization as visualization
from data import modes, modeKeys

print("Initizalizing Microphone...")
microphone.start()

print("Initializing HTTP server...")
server.start()

print("Loading config...")
currVars.load()
led.update()


def multipleIntArr(arr, numb, maxInt = 255, minInt = 0):
    newArr = []
    for i in range(len(arr)):
        channel = arr[i]
        temp = []
        for x in range(len(channel)):
            maxMin = min(max(round(channel[x] * numb), minInt), maxInt)
            temp.append(maxMin)
        newArr.append(temp)
    
    return np.array(newArr)

def  getCurr():
    mode = currVars.getMode()
    
    if not mode in modeKeys:
        return [ None, None, None]


    currMode = modes[mode]
    isVisualizer = currMode["visualizer"] or False
    useFilters = currMode["filters"] or False
    func = currMode["func"]

    return [ isVisualizer, useFilters, func ]

def micCheck(isVis: bool):
        micRunning = microphone.isRunning()
        if isVis and not micRunning:
            microphone.start()

        if not isVis and micRunning:
            microphone.stop()

def main():
    i = 0
    curr_speed = 2500

    isVisualizer, useFilters, func = getCurr()
    isEnergySpeed = currVars.getConfig("energyspeed")
    micCheck(isVisualizer or isEnergySpeed)

    currEnabled = 1.0
    multiplier = currVars.getMultiplier()
    setPrevTime()
    while True:
        enabled = gesture.isEnabled()
        
        if not enabled and currEnabled == 0:
            led.pixels *= 0
            led.update()

            setPrevTime()
            continue
        if i > 50:
            isVisualizer, useFilters, func = getCurr()
            isEnergySpeed = currVars.getConfig("energyspeed")
            micCheck(isVisualizer or isEnergySpeed)
            multiplier = currVars.getMultiplier()
            i = 0

        funcOut = None
        energy = None
        if isVisualizer or isEnergySpeed:
            raw = microphone.read()
            mel = visualization.microphone_update(raw)
            if isVisualizer:
                funcOut = func(mel)
                setPrevTime()
            else:
                energy = getAvgEnergy(mel)
                currVars.setConfig("energyspeed_multiplier", energy)

        if not isVisualizer:
            funcOut = func()
            setPrevTime()

        if useFilters:
            funcOut = applyFilters(funcOut)
            if energy != None:
                funcOut = multipleIntArr(funcOut, energy)


        delta = getDeltaTime()
        if enabled and currEnabled < 1:
            funcOut = multipleIntArr(funcOut, currEnabled)
            currEnabled =  min(currEnabled + delta * curr_speed, 1)
        elif not enabled and currEnabled > 0:
            funcOut = multipleIntArr(funcOut, currEnabled)
            currEnabled = max(0, currEnabled - delta * curr_speed)
        else:
            if multiplier != 1:
                funcOut *= multipleIntArr(funcOut, multiplier)

        led.pixels = funcOut
        led.update()
        i += 1

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