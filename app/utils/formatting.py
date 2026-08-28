def format_bytes_rate(bytes_per_sec: float) -> str:
    units = ["B/s", "KB/s", "MB/s", "GB/s", "TB/s"]
    rate = float(bytes_per_sec)
    unit_index = 0
    while rate >= 1024.0 and unit_index < len(units) - 1:
        rate /= 1024.0
        unit_index += 1
    return f"{rate:.2f} {units[unit_index]}"

def format_bytes_total(total_bytes: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(total_bytes)
    unit_index = 0
    while size >= 1024.0 and unit_index < len(units) - 1:
        size /= 1024.0
        unit_index += 1
    return f"{size:.2f} {units[unit_index]}"

def format_bits_rate(bytes_per_sec: float) -> str:
    bits_per_sec = bytes_per_sec * 8.0
    units = ["bps", "Kbps", "Mbps", "Gbps", "Tbps"]
    rate = float(bits_per_sec)
    unit_index = 0
    while rate >= 1000.0 and unit_index < len(units) - 1:
        rate /= 1000.0
        unit_index += 1
    return f"{rate:.2f} {units[unit_index]}"
