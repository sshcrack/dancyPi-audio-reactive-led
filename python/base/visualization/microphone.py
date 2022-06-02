import time
import numpy as np
import pyaudio

from scipy.ndimage.filters import gaussian_filter1d

import config
import base.visualization.dsp as dsp
from customLogger.log import getLogger

frames_per_buffer = int(config.MIC_RATE / config.FPS)
stream: pyaudio.Stream = None
p: pyaudio.PyAudio = None

overflows = 0
prev_ovf_time = time.time()
logger = getLogger("Microphone")


def start():
    logger.info("Starting Microphone")

    global stream, p
    if stream is not None or p is not None:
        return False

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=config.MIC_RATE,
                    input=True,
                    frames_per_buffer=frames_per_buffer)

    return True


def read():
    global overflows, prev_ovf_time

    try:
        y = np.fromstring(stream.read(frames_per_buffer, exception_on_overflow=False), dtype=np.int16)
        y = y.astype(np.float32)
        stream.read(stream.get_read_available(), exception_on_overflow=False)

        return y
    except IOError:
        overflows += 1
        if time.time() > prev_ovf_time + 1:
            prev_ovf_time = time.time()
            logger.warn('Audio buffer has overflowed {} times'.format(overflows))

        return []


def stop():
    global stream, p

    if stream is None:
        return logger.warn("Trying to stop, but stream is None.")

    logger.info("Stopping microphone")
    stream.stop_stream()
    stream.close()
    p.terminate()

    stream = None
    p = None


def isRunning():
    global stream
    return stream is not None


fft_plot_filter = dsp.ExpFilter(np.tile(1e-1, config.N_FFT_BINS),
                                alpha_decay=0.5, alpha_rise=0.99)
mel_gain = dsp.ExpFilter(np.tile(1e-1, config.N_FFT_BINS),
                         alpha_decay=0.01, alpha_rise=0.99)
mel_smoothing = dsp.ExpFilter(np.tile(1e-1, config.N_FFT_BINS),
                              alpha_decay=0.5, alpha_rise=0.99)
volume = dsp.ExpFilter(config.MIN_VOLUME_THRESHOLD,
                       alpha_decay=0.02, alpha_rise=0.02)
fft_window = np.hamming(int(config.MIC_RATE / config.FPS)
                        * config.N_ROLLING_HISTORY)
prev_fps_update = time.time()

# Number of audio samples to read every time frame
samples_per_frame = int(config.MIC_RATE / config.FPS)

# Array containing the rolling audio sample window
y_roll = np.random.rand(config.N_ROLLING_HISTORY, samples_per_frame) / 1e16


def microphone_update(audio_samples):
    global y_roll, prev_fps_update
    # Normalize samples between 0 and 1

    y = audio_samples / 2.0 ** 15
    # Construct a rolling window of audio samples
    y_roll[:-1] = y_roll[1:]
    y_roll[-1, :] = np.copy(y)
    y_data = np.concatenate(y_roll, axis=0).astype(np.float32)

    vol = np.max(np.abs(y_data))
    if vol < config.MIN_VOLUME_THRESHOLD:
        # Should not react
        return None

    # Transform audio input into the frequency domain
    N = len(y_data)
    N_zeros = 2 ** int(np.ceil(np.log2(N))) - N
    # Pad with zeros until the next power of two
    y_data *= fft_window
    y_padded = np.pad(y_data, (0, N_zeros), mode='constant')
    YS = np.abs(np.fft.rfft(y_padded)[:N // 2])
    # Construct a Mel filterbank from the FFT data
    mel = np.atleast_2d(YS).T * dsp.mel_y.T
    # Scale data to values more suitable for visualization
    # mel = np.sum(mel, axis=0)
    mel = np.sum(mel, axis=0)
    mel = mel ** 2.0
    # Gain normalization
    mel_gain.update(np.max(gaussian_filter1d(mel, sigma=1.0)))
    mel /= mel_gain.value
    mel = mel_smoothing.update(mel)

    # Returning mel for later processing
    return mel


gain = dsp.ExpFilter(np.tile(0.01, config.N_FFT_BINS),
                     alpha_decay=0.001, alpha_rise=0.99)


def getAvgEnergy(mel, pixels: int):
    """Effect that expands from the center with increasing sound energy"""
    global p
    mel = np.copy(mel)
    gain.update(mel)
    mel /= gain.value
    # Scale by the width of the LED strip
    mel *= float((pixels // 2) - 1)
    # Map color channels according to energy in the different freq bands
    scale = 0.9
    r = int(np.mean(mel[:len(mel) // 3] ** scale))
    g = int(np.mean(mel[len(mel) // 3: 2 * len(mel) // 3] ** scale))
    b = int(np.mean(mel[2 * len(mel) // 3:] ** scale))

    return min((r + g + b) / 3 / (pixels / 2) * 2, 2)
