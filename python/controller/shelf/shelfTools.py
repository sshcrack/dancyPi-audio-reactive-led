
mappings = [
    [0, 19],
    [141, 149],

    [20, 39],
    [131, 140],

    [50, 59],
    [40, 49],
    [121, 130],

    [60, 69],
    [102, 120],

    [70, 80],
    [81, 101],
]

mappingIntArr = []
for mapping in mappings:
    s = mapping[1]
    f = mapping[0]
    diff = s - f
    for x in range(diff):
        mappingIntArr.append(f + x)
    mappingIntArr.append(s)

mappingIntArr
def mappingToIndex(i: int):
    return mappingIntArr[i]
