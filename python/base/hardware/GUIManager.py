from typing import Dict

import pygame
import numpy as np
from threading import Thread

from base.controller import GeneralController
from tools.fps import frames_per_second
from tools.tools import clamp


class GUIManager:
    def __init__(self, controllers: Dict[str, GeneralController]):
        self.controllers = controllers
        self.currController = list(controllers.values())[0]
        self.exitSignal = False
        self.shouldRun = True

        self.thread = Thread(target=self.guiThread, daemon=True, name=f"GUI-Thread")
        self.thread.start()
        self.fps_update = frames_per_second()

    def stop(self):
        self.shouldRun = False

    def guiThread(self):
        print(f"GUI thread running with curr id {self.currController.deviceId}")
        clock = pygame.time.Clock()
        pygame.init()

        print("Initializing done. Loading fonts...")
        screen = pygame.display.set_mode((500, 500), pygame.RESIZABLE)
        pygame.display.set_caption(f"LED {self.currController.deviceId}")

        font = pygame.font.SysFont("Calibri", 10)

        def update_fps():
            return font.render(str(round(self.fps_update)), True, pygame.Color("coral"))

        def set_dev():
            return font.render(f"DEV: {self.currController.deviceId}", True, pygame.Color("red"))

        print("While Loop of GUI Thread")
        while self.shouldRun:
            screen.fill((0, 0, 0))
            width = screen.get_width()
            height = screen.get_height()
            currPixels = self.currController.pixels
            N_PIXELS = self.currController.device.N_PIXELS

            rA, gA, bA = currPixels
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

            set_dev()
            self.fps_update = frames_per_second()
            screen.blit(update_fps(), (10, 0))
            pygame.display.flip()
            clock.tick(144)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    values = list(self.controllers.values())
                    index = (values.index(self.currController) + 1) % len(values)

                    self.currController = values[index]
                    pygame.display.set_caption(f"LED {self.currController.deviceId}")
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.exitSignal = True
                    self.shouldRun = False
        pygame.quit()
