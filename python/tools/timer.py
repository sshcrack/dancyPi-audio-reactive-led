from time import time


class Timer:
    def __init__(self):
        self.prevTime = time()
        self.currTime = time()

    def update(self):
        self.prevTime = self.currTime
        self.currTime = time()

    def getDelta(self):
        return self.currTime - self.prevTime
