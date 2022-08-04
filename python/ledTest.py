import json


def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    pos = pos % 255
    if pos < 85:
        return [pos * 3, 255 - pos * 3, 0]
    elif pos < 170:
        pos -= 85
        return [255 - pos * 3, 0, pos * 3]
    else:
        pos -= 170
        return [0, pos * 3, 255 - pos * 3]


arr = []
for i in range(256):
    arr.append(wheel(i))

with open("base/filters/rainbow.json", "w") as f:
    f.write(json.dumps(arr))
