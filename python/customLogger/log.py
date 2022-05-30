import logging
from typing import List


def getLogger(*args: str):
    loggerName = ""
    for i in range(len(args)):
        if i != 0:
            loggerName += ";"
        loggerName += args[i]

    logger = logging.getLogger(loggerName)
    logger.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    logger.addHandler(ch)

    return logger
