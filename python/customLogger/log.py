import logging
import sys
from typing import List

console = logging.StreamHandler(sys.stdout)
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)-13s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger().addHandler(console)


def getLogger(*args: str):
    loggerName = ""
    for i in range(len(args)):
        if i != 0:
            loggerName += ";"
        loggerName += args[i]

    logger = logging.getLogger(loggerName)
    logger.setLevel(logging.DEBUG)

    return logger
