import time
import numpy as np
import pyaudio
import config


frames_per_buffer = int(config.MIC_RATE / config.FPS)
stream = None
p = None

overflows = 0
prev_ovf_time = time.time()


def start():
    global stream, p
    if stream != None or p != None:
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
            print('Audio buffer has overflowed {} times'.format(overflows))

        return [ ]

def stop():
    global stream, p

    if stream == None:
        return print("Stream is None.")

    print("Closing stream.")
    stream.stop_stream()
    stream.close()
    p.terminate()

    stream = None
    p = None