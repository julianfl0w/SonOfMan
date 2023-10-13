import stun
import uuid
import json
import requests
import asyncio

def getInventory():
    # Google's STUN server
    stun_host = "stun.l.google.com"
    stun_port = 19302  # default STUN port

    # Get the external IP and the NAT type
    nat_type, external_ip, external_port = stun.get_ip_info(stun_host=stun_host, stun_port=stun_port)

    mac_num = uuid.getnode()
    mac_address = ':'.join(('%012X' % mac_num)[i:i+2] for i in range(0, 12, 2))


    # Store all values in a dictionary
    network_info = {
        "NAT_Type": nat_type,
        "External_IP": external_ip,
        "External_Port": external_port,
        "MAC_Address": mac_address
    }

    return network_info
print(json.dumps(getInventory(), indent=2))
