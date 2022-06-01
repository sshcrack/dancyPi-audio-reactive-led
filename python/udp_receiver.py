import socket
import board
from neopixel import NeoPixel

PIXELS = 16

ip = "0.0.0.0"
port = 6189

listeningAddress = (ip, port)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(listeningAddress)

BUFF_LENGTH = 1024

strip = NeoPixel(board.D18, PIXELS)

while True:
    v, _ = s.recvfrom(BUFF_LENGTH)
    for i in range(0, len(v), 4):
        led = v[i]
        r = v[i + 1]
        g = v[i + 2]
        b = v[i + 3]
        strip[led] = (r, g, b)
