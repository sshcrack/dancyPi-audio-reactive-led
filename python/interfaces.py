from netifaces import interfaces, ifaddresses, AF_INET


def getIPs():
    ip_list = []
    for interface in interfaces():
        ifaddressList = ifaddresses(interface)
        if AF_INET not in ifaddressList.keys():
            continue

        for link in ifaddressList[AF_INET]:
            ip_list.append(link['addr'])
    return ip_list
