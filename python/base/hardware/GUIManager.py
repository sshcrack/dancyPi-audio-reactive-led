import pygame
import numpy as np
from threading import Thread
from base.hardware.configDict import *
from tools.fps import frames_per_second
from tools.tools import clamp
from random import random


class GUIManager:
    def __init__(self, config: GeneralLEDConfig, deviceId: str):
        self.config = config
        self.deviceId = deviceId
        self.fps_update = frames_per_second()
        self.pixels = np.tile(1, (3, config.N_PIXELS))

        self.exitSignal = False
        self.shouldRun = True

        self.thread = Thread(target=self.guiThread, daemon=True)
        self.thread.start()

    def stop(self):
        self.shouldRun = False

    def update(self, p: np.ndarray):
        self.pixels = p
        self.fps_update = frames_per_second()

    def guiThread(self):
        clock = pygame.time.Clock()
        pygame.init()

        screen = pygame.display.set_mode((500, 500), pygame.RESIZABLE)
        pygame.display.set_caption(f"LED {self.deviceId}")

        font = pygame.font.SysFont("Arial", 10)

        def update_fps():
            return font.render(str(round(self.fps_update)), True, pygame.Color("coral"))

        while self.shouldRun:
            screen.fill((0, 0, 0))
            width = screen.get_width()
            height = screen.get_height()

            rA, gA, bA = self.pixels
            pixel_width = width / self.config.N_PIXELS
            for i in range(self.config.N_PIXELS):
                r = clamp(0, int(rA[i]), 255)
                g = clamp(0, int(gA[i]), 255)
                b = clamp(0, int(bA[i]), 255)

                xStart = i * pixel_width
                xEnd = (i + 1) * pixel_width
                y = 0
                pos = (xStart, y, xEnd, y + height)
                pygame.draw.rect(screen, [r, g, b], pygame.Rect(pos))

            pygame.draw.rect(screen, [random() * 255, random() * 255, random() * 255], pygame.Rect((0, 0, 10, 10)))
            screen.blit(update_fps(), (10, 0))
            pygame.display.flip()
            clock.tick(144)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.exitSignal = True
                    self.shouldRun = False
