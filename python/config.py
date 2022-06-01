"""Settings for audio reactive LED strip"""
from __future__ import print_function
from __future__ import division

import os

PORT = 6789
BIND_ADDRESS = '0.0.0.0'

"""Device used to control LED strip. Must be 'pi',  'esp8266' or 'blinkstick'
'esp8266' means that you are using an ESP8266 module to control the LED strip
and commands will be sent to the ESP8266 over WiFi.
'pi' means that you are using a Raspberry Pi as a standalone unit to process
audio input and control the LED strip directly.
'blinkstick' means that a BlinkstickPro is connected to this PC which will be used
to control the leds connected to it.
"""


GESTURE_SENSOR_ENABLED = False
"""Whether a Groove Gesture Sensor is connected to the pi"""


GAMMA_TABLE_PATH = os.path.join(os.path.dirname(__file__), 'base', 'visualization', 'gamma_table.npy')
"""Location of the gamma correction table"""

MIC_RATE = 48000
"""Sampling frequency of the microphone in Hz"""

DISPLAY_FPS = True

FPS = 100
"""Desired refresh rate of the visualization (frames per second)

FPS indicates the desired refresh rate, or frames-per-second, of the audio
visualization. The actual refresh rate may be lower if the computer cannot keep
up with desired FPS value.

Higher framerates improve "responsiveness" and reduce the latency of the
visualization but are more computationally expensive.

Low framerates are less computationally expensive, but the visualization may
appear "sluggish" or out of sync with the audio being played if it is too low.

The FPS should not exceed the maximum refresh rate of the LED strip, which
depends on how long the LED strip is.
"""
#TODO
# _max_led_FPS = int(((N_PIXELS * 30e-6) + 50e-6)**-1.0)
# assert FPS <= _max_led_FPS, 'FPS must be <= {}'.format(_max_led_FPS)

MIN_FREQUENCY = 200
"""Frequencies below this value will be removed during audio processing"""

MAX_FREQUENCY = 12000
"""Frequencies above this value will be removed during audio processing"""

N_FFT_BINS = 24
"""Number of frequency bins to use when transforming audio to frequency domain

Fast Fourier transforms are used to transform time-domain audio data to the
frequency domain. The frequencies present in the audio signal are assigned
to their respective frequency bins. This value indicates the number of
frequency bins to use.

A small number of bins reduces the frequency resolution of the visualization
but improves amplitude resolution. The opposite is true when using a large
number of bins. More bins is not always better!

There is no point using more bins than there are pixels on the LED strip.
"""

N_ROLLING_HISTORY = 2
"""Number of past audio frames to include in the rolling window"""

MIN_VOLUME_THRESHOLD = 1e-7
"""No music visualization displayed if recorded audio volume below threshold"""
