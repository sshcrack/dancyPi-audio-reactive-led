from interfaces import getIPs
from config import BIND_ADDRESS, PORT

ips = getIPs()
last_addr = ".".join(BIND_ADDRESS.split(".")[:-1])

matching_ips = ips
if addr != "0.0.0.0":
    matching_ips = [ "127.0.0.1"]
    for ip in ips:
        if last_addr in ip:
            matching_ips.append(ip)

print("Server should be listening on if server is running:")
for ip in ips:
    print(f"    http://{ip}:{PORT}")
