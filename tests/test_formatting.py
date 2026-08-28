from app.utils.formatting import format_bytes_rate, format_bytes_total, format_bits_rate

def test_format_bytes_rate():
    assert format_bytes_rate(512) == "512.00 B/s"
    assert format_bytes_rate(1024) == "1.00 KB/s"
    assert format_bytes_rate(1536) == "1.50 KB/s"
    assert format_bytes_rate(1048576) == "1.00 MB/s"
    assert format_bytes_rate(1073741824) == "1.00 GB/s"

def test_format_bytes_total():
    assert format_bytes_total(512) == "512.00 B"
    assert format_bytes_total(1024) == "1.00 KB"
    assert format_bytes_total(1048576) == "1.00 MB"
    assert format_bytes_total(1073741824) == "1.00 GB"

def test_format_bits_rate():
    assert format_bits_rate(125) == "1.00 Kbps"
    assert format_bits_rate(125000) == "1.00 Mbps"
    assert format_bits_rate(125000000) == "1.00 Gbps"
