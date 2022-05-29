import numpy as np


def multipleIntArr(arr, numb, max_int=255, min_int=0):
    """Multiple the array by a given number and don't exceed the range given"""
    newArr = []
    for i in range(len(arr)):
        channel = arr[i]
        temp = []
        for x in range(len(channel)):
            maxMin = min(max(round(channel[x] * numb), min_int), max_int)
            temp.append(maxMin)
        newArr.append(temp)

    return np.array(newArr)