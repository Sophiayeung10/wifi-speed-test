import pytest
from wifi_telemetry import get_wifi_telemetry, measure_gateway_latency

# Validation Thresholds
MIN_RSSI_DBM = -70.0  # Acceptable indoor RF signal level
MIN_PHY_RATE_MBPS = 150.0  # Minimum hardware PHY link rate
MAX_PACKET_LOSS_PCT = 0.0  # Zero tolerance for local RF packet loss


def test_wifi_rf_signal_strength():
    """Verify RF signal level meets minimum threshold for reliable connection."""
    telemetry = get_wifi_telemetry()
    assert (
        telemetry["rssi_dbm"] is not None
    ), "Failed to read Wi-Fi adapter telemetry"
    print(
        f"\n[RF Check] Measured RSSI: {telemetry['rssi_dbm']} dBm ({telemetry['signal_pct']}%)"
    )
    assert (
        telemetry["rssi_dbm"] >= MIN_RSSI_DBM
    ), f"RF Signal too weak: {telemetry['rssi_dbm']} dBm < {MIN_RSSI_DBM} dBm"


def test_wifi_phy_negotiated_rate():
    """Verify hardware network card negotiated link rate (PHY layer)."""
    telemetry = get_wifi_telemetry()
    assert (
        telemetry["tx_rate_mbps"] is not None
    ), "Failed to read PHY link rate"
    print(
        f"\n[PHY Check] Protocol: {telemetry['radio_type']} | Channel: {telemetry['channel']} | Link Rate: {telemetry['tx_rate_mbps']} Mbps"
    )
    assert (
        telemetry["tx_rate_mbps"] >= MIN_PHY_RATE_MBPS
    ), f"PHY link rate below spec: {telemetry['tx_rate_mbps']} Mbps < {MIN_PHY_RATE_MBPS} Mbps"


def test_gateway_rf_link_stability():
    """Verify zero packet loss over local RF link to rule out wireless interference."""
    res = measure_gateway_latency(gateway_ip="192.168.1.1", count=10)
    print(f"\n[Link Stability] Packet Loss: {res['packet_loss_pct']}%")
    assert (
        res["packet_loss_pct"] <= MAX_PACKET_LOSS_PCT
    ), f"Excessive RF packet loss detected: {res['packet_loss_pct']}%"
