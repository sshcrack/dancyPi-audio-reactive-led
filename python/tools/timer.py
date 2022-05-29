from time import time

_time_prev = time()


def getPrevTime():
    global _time_prev
    return _time_prev


def setPrevTime():
    global _time_prev
    _time_prev = time()


class Timer:
    def __init__(self):
        self.currTime = time()

    def update(self):
        self.currTime = time()

    def getDelta(self):
        return time() - self.currTime
