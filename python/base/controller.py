import os
import sys
import threading
import traceback
from typing import Any, Dict

from time import time

import numpy as np

import config
from base.hardware.configDict import loadDeviceConfig
from customLogger.log import getLogger
from httpserver.api.apiServer import APIServer
from tools.interfaces import find_free_port
from tools.nparray import multipleIntArr
from base.visualization.dsp import ExpFilter
from tools.fps import frames_per_second
from base.configManager import ConfigManager
from tools.energyspeed import getAvgEnergy
from tools.timer import Timer
from tools.tools import clamp
from base.hardware.GUIManager import GUIManager
from base.hardware.LEDManager import LEDManager
from base.modes.full import FullMode
from base.filters.hex import HexFilter
from base.filters.normal import NormalMode
from base.GeneralMode import GeneralMode
from base.GeneralFilter import GeneralFilter
from base.filters.rainbow import RainbowMode

defaultMode = "full"
defaultFilter = "normal"
preventLEDThreadUpdate = "--update-sync" in sys.argv


class GeneralController:
    energy_filter: ExpFilter

    def __init__(self, deviceId: str, modes: Dict[str, Any], filters: Dict[str, Any], configDefaults=None, gui=False):
        self.shouldExit = False
        self.initialized = False
        self.timer = Timer()

        defaultModes = {
            "full": FullMode
        }

        defaultFilters = {
            "hex": HexFilter,
            "normal": NormalMode,
            "rainbow": RainbowMode
        }

        if configDefaults is None:
            configDefaults = {}

        self.minimalMode = "--minimal" in sys.argv
        self.deviceId = deviceId
        self.logger = getLogger("GeneralController", deviceId)
        self.device = loadDeviceConfig(deviceId)
        self.config = ConfigManager(deviceId, configDefaults)
        self.enabled = self.config.get("enabled")

        self.energySense = clamp(0.0001, self.config.get("energy_sensitivity", .99), .99)
        self.isEnergySpeed = self.config.get("energy_speed", False)
        self.isEnergyBrightness = self.config.get("energy_brightness", False)
        self.energyBrightnessMult = self.config.get("energy_brightness_mult", 1)

        self.energy_filter = ExpFilter(
            1,
            alpha_decay=self.energySense,
            alpha_rise=.99
        )

        self.constructorModes = {**defaultModes, **modes}
        self.constructorFilters = {**defaultFilters, **filters}
        self.modes: Dict[str, GeneralMode] = {}
        self.filters: Dict[str, GeneralFilter] = {}

        for keyMode in list(self.constructorModes.keys()):
            self.logger.debug(f"Loading mode {keyMode}...")
            self.modes[keyMode] = self.constructorModes[keyMode](self)
            self.logger.debug(f"Mode {keyMode} loaded. {self.modes[keyMode]}")

        for keyFilter in list(self.constructorFilters.keys()):
            self.logger.debug(f"Loading filter {keyFilter}...")
            self.filters[keyFilter] = self.constructorFilters[keyFilter](self)

        self.pixels = np.tile(1, (3, self.device.N_PIXELS))

        self.currMode = self.config.getMode()
        if self.currMode is None:
            self.currMode = defaultMode
        self.currFilter = self.config.get("filter_mode", defaultFilter)
        # How far to enable animation state has proceeded. 1 = normal, 0 = off
        self.currEnableAnimationState = 1.0
        self.prev_fps_update = time()

        try:
            self.led = LEDManager(self.device, self.deviceId)
        except ImportError as e:
            self.logger.warn(f"Could not load LEDManager. Disabling leds.")
            traceback.print_exc()
            self.led = None
        except RuntimeError as e:
            self.logger.warn(f"LEDManager could not be loaded. Device is not enabled")
            traceback.print_exc()
            self.led = None

        self.gui = None
        if gui:
            try:
                self.gui = GUIManager(self.device, deviceId)
            except Exception as e:
                self.logger.warn(f"Could not start GUI Manager. Disabling...")
                traceback.print_exc()

        if self.gui is None and self.led is None:
            raise ValueError("Neither GUI nor LEDS could be loaded. Stopping.")

        if not self.minimalMode:
            self.api = APIServer(self)
            self.api.serve("127.0.0.1", find_free_port())
        else:
            self.api = None
        self.mel = None

    def shutdown(self):
        self.shouldExit = True
        self.logger.info("Shutting down")
        self.config.save()
        if self.led is not None:
            self.led.stop(self.pixels)
        if self.gui is not None:
            self.gui.shouldRun = False
        if self.api is not None:
            self.api.shutdown()

    def updateVars(self):
        self.enabled = self.config.get("enabled")
        self.energySense = self.config.get("energy_sensitivity", .99)
        self.isEnergySpeed = self.config.get("energy_speed", False)
        self.isEnergyBrightness = self.config.get("energy_brightness", False)
        self.energyBrightnessMult = self.config.get("energy_brightness_mult", 1)
        self.currMode = self.config.getMode()
        if self.currMode is None:
            self.currMode = defaultMode
        self.currFilter = self.config.get("filter_mode", defaultFilter)

    def run(self):
        if round(time()) % 3 == 0:
            if self.gui is not None and self.gui.exitSignal:
                self.shouldExit = True
            self.updateVars()

        if not self.enabled and self.currEnableAnimationState == 0:
            self.pixels *= 0
            self.updateLeds()

            self.timer.update()
            return

        isVisualizer, useFilters, filterClass, modeClass = self.getCurr()

        energy, outPixels = self.calculateModePixels(isVisualizer, modeClass)
        if energy is None and outPixels is None:
            return

        if useFilters:
            outPixels = filterClass.run(outPixels)
            if energy is not None and self.isEnergyBrightness:
                outPixels = self.calculateEnergyBrightness(outPixels, energy)

        outPixels = self.applyEnableAnimation(outPixels)
        outPixels = self.postProcessPixels(outPixels)
        self.pixels = outPixels

        if not preventLEDThreadUpdate:
            th = threading.Thread(target=lambda: self.updateLeds(outPixels), name=f"LED_UPDATE_{id(time())}",
                                  daemon=False)
            th.start()
        else:
            self.updateLeds()
        if config.DISPLAY_FPS:
            fps = frames_per_second()
            if time() - 0.5 > self.prev_fps_update:
                self.prev_fps_update = time()
                self.logger.debug('] FPS {:.0f} / {:.0f}'.format(fps, config.FPS))

    def postProcessPixels(self, data: np.ndarray):
        return data

    def updateLeds(self, p=None):
        if p is None:
            p = self.pixels
        if self.led is not None:
            self.led.update(p)
        if self.gui is not None:
            self.gui.update(p)

    def applyEnableAnimation(self, outPixels: np.ndarray):
        delta = self.timer.getDelta()
        animState = self.currEnableAnimationState

        if self.enabled and animState < 1:
            outPixels = multipleIntArr(outPixels, animState)
            animState = min(animState + delta * 8, 1)
        elif not self.enabled and animState > 0:
            outPixels = multipleIntArr(outPixels, animState)
            animState = max(0, animState - delta * 3)

        self.currEnableAnimationState = animState
        return outPixels

    def calculateEnergyBrightness(self, outPixels: np.ndarray, energy: float):
        return multipleIntArr(outPixels, energy * self.energyBrightnessMult)

    def calculateModePixels(self, isVisualizer: bool, modeClass):
        energy = None
        modePixelsOut = None

        shouldReadMicrophone = isVisualizer or self.isEnergyBrightness or self.isEnergySpeed
        if shouldReadMicrophone:
            if self.mel is None:
                return None, None
            if isVisualizer:
                modePixelsOut = modeClass.run(self.mel)
            else:
                avgEnergy = getAvgEnergy(self.mel, self.device.N_PIXELS)
                energy = self.energy_filter.update(avgEnergy)
                self.config.set("energy_curr", energy)

        if not isVisualizer:
            modePixelsOut = modeClass.run(None)
        self.timer.update()

        return energy, modePixelsOut

    def setEnabled(self, enabled):
        self.enabled = enabled
        self.device.enabled = enabled

    def getCurr(self):
        modeClass = self.modes[self.currMode]
        filterClass = self.filters[self.currFilter]

        if modeClass is None:
            modeClass = self.modes[defaultMode]
        if filterClass is None:
            filterClass = self.filters[defaultFilter]

        modeData = modeClass.data
        isVisualizer = modeData["visualizer"]
        useFilters = modeData["filters"]
        return (
            isVisualizer,
            useFilters,
            filterClass,
            modeClass
        )
