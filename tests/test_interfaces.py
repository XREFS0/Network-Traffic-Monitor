from app.network.interfaces import get_network_interfaces
from app.models.traffic import InterfaceInfo

def test_get_network_interfaces():
    ifaces = get_network_interfaces()
    assert isinstance(ifaces, list)
    for iface in ifaces:
        assert isinstance(iface, InterfaceInfo)
        assert iface.name
        assert iface.display_name
        assert isinstance(iface.status, bool)
