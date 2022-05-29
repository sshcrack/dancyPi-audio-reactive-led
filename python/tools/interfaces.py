from netifaces import interfaces, ifaddresses, AF_INET
import socket
from contextlib import closing


def getIPs():
    ip_list = []
    for interface in interfaces():
        ifaddressList = ifaddresses(interface)
        if AF_INET not in ifaddressList.keys():
            continue

        for link in ifaddressList[AF_INET]:
            ip_list.append(link['addr'])
    return ip_list


def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]
