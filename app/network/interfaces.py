import socket
import psutil
from typing import List, Dict
from app.models.traffic import InterfaceInfo

def get_network_interfaces() -> List[InterfaceInfo]:
    interfaces = []
    addrs = psutil.net_if_addrs()
    stats = psutil.net_if_stats()

    for name, addr_list in addrs.items():
        ipv4_val = None
        ipv6_val = None
        mac_val = None
        
        for addr in addr_list:
            if addr.family == socket.AF_INET:
                ipv4_val = addr.address
            elif addr.family == getattr(socket, "AF_INET6", -1):
                ipv6_val = addr.address.split("%")[0]
            elif addr.family in (getattr(psutil, "AF_LINK", -1), getattr(socket, "AF_LINK", -1), -1):
                mac_val = addr.address
        
        stat = stats.get(name)
        status = False
        speed = None
        
        if stat:
            status = stat.isup
            speed = stat.speed if stat.speed > 0 else None
            
        display_name = name
        
        interfaces.append(
            InterfaceInfo(
                name=name,
                display_name=display_name,
                status=status,
                mac_address=mac_val,
                ipv4_address=ipv4_val,
                ipv6_address=ipv6_val,
                link_speed_mbps=speed
            )
        )
    return sorted(interfaces, key=lambda x: (x.status, x.name), reverse=True)
