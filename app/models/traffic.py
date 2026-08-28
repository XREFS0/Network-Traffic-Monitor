from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class InterfaceInfo:
    name: str
    display_name: str
    status: bool
    mac_address: Optional[str] = None
    ipv4_address: Optional[str] = None
    ipv6_address: Optional[str] = None
    link_speed_mbps: Optional[float] = None

@dataclass(frozen=True)
class ThroughputStats:
    bytes_sent: int
    bytes_recv: int
    bytes_sent_per_sec: float
    bytes_recv_per_sec: float
    packets_sent: int
    packets_recv: int
    packets_sent_per_sec: float
    packets_recv_per_sec: float
    errors_in: int
    errors_out: int
    drop_in: int
    drop_out: int

@dataclass(frozen=True)
class PacketSummary:
    protocol: str
    source_ip: str
    dest_ip: str
    source_port: Optional[int]
    dest_port: Optional[int]
    size: int
    timestamp: float
