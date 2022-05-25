import pygame
import numpy as np
import sys
from threading import Thread

from config import N_PIXELS

pixels = np.tile(1, (3, N_PIXELS))

shouldRun = True
exitSignal = False


def update(p: np.ndarray):
    global pixels
    pixels = p


def clamp(min_numb: int, value: int, max_numb: int):
    if value < min_numb:
        return min_numb
    if value > max_numb:
        return max_numb

    return value


def guiThread():
    global exitSignal, shouldRun
    clock = pygame.time.Clock()
    pygame.init()
    screen = pygame.display.set_mode((500, 500), pygame.RESIZABLE)
    pygame.display.set_caption('LED GUI')

    font = pygame.font.SysFont("Arial", 18)

    def update_fps():
        fps = str(int(clock.get_fps()))
        fps_text = font.render(fps, 1, pygame.Color("coral"))
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

        screen.blit(update_fps(), (10, 0))
        pygame.display.flip()
        clock.tick(60)

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
