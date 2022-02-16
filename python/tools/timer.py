from time import time


_time_prev = time()

def getPrevTime():
    global _time_prev
    return _time_prev

def setPrevTime():
    global _time_prev
    _time_prev = time()