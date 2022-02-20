import subprocess


rc = subprocess.call(['which', 'ifconfig'])
if rc != 0:
    print 'Make sure to be running as root'

def getIPs():
    out = subprocess.run([ "sudo", "ifconfig", "-a"], capture_output=True).stdout.decode("utf-8")
    newLines = filter(lambda e: "inet " in e, out.split("\n"))
    newLines = map(lambda e: e.split(" "), newLines)
    addresses = []

    for el in newLines:
        for x in range(len(el)):
            curr = el[x]
            prevIndex = x -1
            if(prevIndex < 0):
                continue

            prev = el[prevIndex]
            if "inet" in prev:
                addresses.append(curr)
    return addresses
