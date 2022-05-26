import math
import random
import time

import mpmath
import pygame
import numpy as np
from threading import Thread

import config
from config import N_PIXELS
from tools.fps import frames_per_second
from tools.tools import clamp

pixels = np.tile(1, (3, N_PIXELS))

shouldRun = True
exitSignal = False

fps_update = frames_per_second()


def update(p: np.ndarray):
    global pixels, fps_update
    pixels = p
    fps_update = frames_per_second()


def guiThread():
    global exitSignal, shouldRun, fps_update
    clock = pygame.time.Clock()
    pygame.init()
    screen = pygame.display.set_mode((500, 500), pygame.RESIZABLE)
    pygame.display.set_caption('LED GUI')

    font = pygame.font.SysFont("Arial", 18)

    def update_fps():
        fps_text = font.render(str(round(fps_update)), True, pygame.Color("coral"))
        return fps_text

    while shouldRun:
        screen.fill((0, 0, 0))
        width = screen.get_width()
        height = screen.get_height()

        rA, gA, bA = pixels
        pixel_width = width / N_PIXELS
        for i in range(N_PIXELS):
            r = clamp(0, int(rA[i]), 255)
            g = clamp(0, int(gA[i]), 255)
            b = clamp(0, int(bA[i]), 255)

            xStart = i * pixel_width
            xEnd = (i + 1) * pixel_width
            y = 0
            pos = (xStart, y, xEnd, y + height)
            pygame.draw.rect(screen, [r, g, b], pygame.Rect(pos))

        pygame.draw.rect(screen, [random.random() * 255, random.random() * 255, random.random() * 255], pygame.Rect((0, 0, 10, 10)))
        screen.blit(update_fps(), (10, 0))
        pygame.display.flip()
        clock.tick(150)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exitSignal = True
                shouldRun = False


thread1 = Thread(target=guiThread, daemon=True)


def stop():
    global shouldRun
    shouldRun = False


def start():
    thread1.start()
