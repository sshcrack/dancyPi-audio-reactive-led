import time
import traceback

import numpy as np

import config as globalConfig
import socket
from base.hardware.configDict import *
from customLogger.log import getLogger

logger = getLogger("LEDManager")
blinkstickAvailable = False
try:
    import signal
    import sys

    from blinkstick import blinkstick

    blinkstickAvailable = True
except ImportError as e:
    traceback.print_exc()
    logger.warn("Could not import blinkstick, 'blinkstick' as device can not be used")

rpiAvailable = False
try:
    from rpi_ws281x import *

    rpiAvailable = True
except ImportError as e:
    traceback.print_exc()
    logger.warn("Could not import rpi_ws281x, 'pi' as device wont be available")

_gamma = np.load(globalConfig.GAMMA_TABLE_PATH)
"""Gamma lookup table used for nonlinear brightness correction"""


class LEDManager:
    def __init__(self, config: GeneralLEDConfig, devId: str):
        self.config = config
        self.logger = getLogger("LEDManager", devId)

        self._prev_pixels = np.tile(253, (3, config.N_PIXELS))
        """Pixel values that were most recently displayed on the LED strip"""

        self.pixels = np.tile(1, (3, config.N_PIXELS))
        """Pixel values for the LED strip"""

        self.logger.debug(f"Constructed prevPixels with length of {config.N_PIXELS}")
        dev = self.config.DEVICE

        if dev == "blinkstick":
            if not blinkstickAvailable:
                raise RuntimeError("Blinkstick not enabled. Look at log to fix")

            # Will turn all leds off when invoked.
            def signal_handler(signal, frame):
                all_off = [0] * (config.N_PIXELS * 3)
                self.stick.set_led_data(0, all_off)
                sys.exit(0)

            self.stick = blinkstick.find_first()
            # Create a listener that turns the leds off when the program terminates
            signal.signal(signal.SIGTERM, signal_handler)
            signal.signal(signal.SIGINT, signal_handler)
        elif dev == "pi":
            if not rpiAvailable:
                raise RuntimeError("RPI Device not enabled. Look at log to fix")
            self.strip = Adafruit_NeoPixel(config.N_PIXELS, config.LED_PIN,
                                           config.LED_FREQ_HZ, config.LED_DMA,
                                           config.LED_INVERT, config.BRIGHTNESS)
            self.strip.begin()
        elif "esp8266":
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def _update_esp8266(self, pixels: np.ndarray):
        """Sends UDP packets to ESP8266 to update LED strip values

        The ESP8266 will receive and decode the packets to determine what values
        to display on the LED strip. The communication protocol supports LED strips
        with a maximum of 256 LEDs.

        The packet encoding scheme is:
            |i|r|g|b|
        where
            i (0 to 255): Index of LED to change (zero-based)
            r (0 to 255): Red value of LED
            g (0 to 255): Green value of LED
            b (0 to 255): Blue value of LED
        """
        espConfig: ESPConfig = self.config

        # Truncate values and cast to integer
        pixels = np.clip(pixels, 0, 255).astype(int)

        # Optionally apply gamma correct io
        p = _gamma[pixels] if espConfig.SOFTWARE_GAMMA_CORRECTION else np.copy(pixels)
        MAX_PIXELS_PER_PACKET = 126

        # Pixel indices
        idx = range(pixels.shape[1])
        idx = [i for i in idx if not np.array_equal(p[:, i], self._prev_pixels[:, i])]
        n_packets = len(idx) // MAX_PIXELS_PER_PACKET + 1
        idx = np.array_split(idx, n_packets)

        for packet_indices in idx:
            m = []
            for i in packet_indices:
                m.append(i)  # Index of pixel to change
                m.append(p[0][i])  # Pixel red value
                m.append(p[1][i])  # Pixel green value
                m.append(p[2][i])  # Pixel blue value
            m = bytes(m)
            self._sock.sendto(m, (espConfig.UDP_IP, espConfig.UDP_PORT))
        self._prev_pixels = np.copy(p)

    def _update_blinkstick(self, pixels: np.ndarray):
        """Writes new LED values to the Blinkstick.
            This function updates the LED strip with new values.
        """

        # Truncate values and cast to integer
        pixels = np.clip(pixels, 0, 255).astype(int)
        # Optional gamma correction
        p = _gamma[pixels] if self.config.SOFTWARE_GAMMA_CORRECTION else np.copy(pixels)
        # Read the rgb values
        r = p[0][:].astype(int)
        g = p[1][:].astype(int)
        b = p[2][:].astype(int)

        # create array in which we will store the led states
        newstrip = [None] * (self.config.N_PIXELS * 3)

        for i in range(self.config.N_PIXELS):
            # blinkstick uses GRB format
            newstrip[i * 3] = g[i]
            newstrip[i * 3 + 1] = r[i]
            newstrip[i * 3 + 2] = b[i]
        # send the data to the blinkstick
        self.stick.set_led_data(0, newstrip)

    def _update_pi(self, pixels: np.ndarray):
        """Writes new LED values to the Raspberry Pi's LED strip

        Raspberry Pi uses the rpi_ws281x to control the LED strip directly.
        This function updates the LED strip with new values.
        """
        # G R B order
        pixels = np.array([pixels[1], pixels[0], pixels[2]])

        # Truncate values and cast to integer
        pixels = np.clip(pixels, 0, 255).astype(int)
        # Optional gamma correction
        p = _gamma[pixels] if self.config.SOFTWARE_GAMMA_CORRECTION else np.copy(pixels)
        # Encode 24-bit LED values in 32 bit integers
        r = np.left_shift(p[0][:].astype(int), 8)
        g = np.left_shift(p[1][:].astype(int), 16)
        b = p[2][:].astype(int)
        rgb = np.bitwise_or(np.bitwise_or(r, g), b)
        # Update the pixels

        for i in range(self.config.N_PIXELS):
            # Ignore pixels if they haven't changed (saves bandwidth)
            if np.array_equal(p[:, i], self._prev_pixels[:, i]):
                continue

            self.strip._led_data[i] = int(rgb[i])
        self._prev_pixels = np.copy(p)
        self.strip.show()

    def update(self, pixels: np.ndarray):
        if pixels.shape[1] != self.config.N_PIXELS:
            self.logger.warn(f"Invalid pixel shape {pixels.shape} (has to have (3, {self.config.N_PIXELS}). Skipping")
            return

        dev = self.config.DEVICE
        self.pixels = pixels

        if dev == "esp8266":
            self._update_esp8266(pixels)
        elif dev == "pi":
            self._update_pi(pixels)
        elif dev == "blinkstick":
            self._update_blinkstick(pixels)
        else:
            raise ValueError("Invalid device given in config")

    def stop(self, pixels):
        pixels *= 0
        # To ensure even on udp all pixels are turned off
        for i in range(5):
            self.update(pixels)
            time.sleep(0.01)