import platform
import re
import subprocess


def get_wifi_telemetry() -> dict:
    """Extracts physical Layer (PHY/MAC) Wi-Fi telemetry from the local NIC."""
    os_name = platform.system()
    telemetry = {
        "signal_pct": None,
        "rssi_dbm": None,
        "tx_rate_mbps": None,
        "channel": None,
        "radio_type": None,
    }

    if os_name == "Windows":
        try:
            output = subprocess.check_output(
                ["netsh", "wlan", "show", "interfaces"], encoding="utf-8"
            )
            signal_match = re.search(r"Signal\s*:\s*(\d+)%", output)
            rate_match = re.search(
                r"Receive rate \(Mbps\)\s*:\s*([\d.]+)", output
            )
            radio_match = re.search(r"Radio type\s*:\s*(.+)", output)
            channel_match = re.search(r"Channel\s*:\s*(\d+)", output)

            if signal_match:
                pct = int(signal_match.group(1))
                telemetry["signal_pct"] = pct
                # Rough approximation: RSSI (dBm) ≈ (Signal % / 2) - 100
                telemetry["rssi_dbm"] = (pct / 2) - 100
            if rate_match:
                telemetry["tx_rate_mbps"] = float(rate_match.group(1))
            if radio_match:
                telemetry["radio_type"] = radio_match.group(1).strip()
            if channel_match:
                telemetry["channel"] = int(channel_match.group(1))
        except Exception as e:
            print(f"Error querying netsh: {e}")

    return telemetry


def measure_gateway_latency(gateway_ip="192.168.1.1", count=10) -> dict:
    """Measures RF link latency and packet loss to local default gateway."""
    cmd = ["ping", "-n" if platform.system() == "Windows" else "-c", str(count), gateway_ip]
    try:
        output = subprocess.check_output(cmd, encoding="utf-8")
        # Extract packet loss
        loss_match = re.search(r"\((\d+)% loss\)", output)
        packet_loss = int(loss_match.group(1)) if loss_match else 0
        return {"packet_loss_pct": packet_loss, "raw_output": output}
    except Exception as e:
        return {"packet_loss_pct": 100, "error": str(e)}
