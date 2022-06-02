#!/bin/python3
import socket
from threading import Thread
import board
from neopixel import NeoPixel


PIXELS = 150

#ip      = "127.0.0.1"
ip = "0.0.0.0"
port    = 6189

listeningAddress = (ip, port)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(listeningAddress)

BUFF_LENGTH = 1024

strip = NeoPixel(board.D18, PIXELS, auto_write=False)


def show():
    strip.show()

try:
    while(True):
        v, _ = s.recvfrom(BUFF_LENGTH)
        for i in range(0, len(v), 4):
            led = v[i]
            r = v[i +1]
            g = v[i +2]
            b = v[i +3]

            if led >= PIXELS:
                continue
            strip[led] = (r, g, b)
        th = Thread(target=show, name=f"UDP_RECEIVER")
        th.start()
except KeyboardInterrupt:
    pass
finally:
    for i in range(PIXELS):
        strip[i] = (0, 0, 0)
    strip.show()
