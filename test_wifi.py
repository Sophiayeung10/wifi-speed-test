"""Wi-Fi speed check written with pytest + requests.
The speed test FAILS if the download speed is below 100 Mbps.
Run it with: pytest
"""
import time
import requests

GITHUB_PROFILE_URL = "https://github.com/Sophiayeung10" #my github portfolio, answers with status 200
SPEED_TEST_URL = "https://speed.cloudflare.com/__down?bytes=50000000"   # a 50 MB test file
MIN_SPEED_MBPS = 100     # below this, the test will fail
MAX_TEST_SECONDS = 15    # stop early on a slow connection so the test never hangs


def measure_download_speed_mbps(url=SPEED_TEST_URL, max_seconds=MAX_TEST_SECONDS):
    """Download a file and return the speed in megabits per second (Mbps)."""
    response = requests.request(method="GET", url=url, stream=True, timeout=10)
    response.raise_for_status()

    total_bytes = 0
    start = time.perf_counter()          # start the clock once the download begins
    for chunk in response.iter_content(chunk_size=64 * 1024):
        total_bytes += len(chunk)
        if time.perf_counter() - start > max_seconds:
            break                        # too slow, stop and use what we have
    elapsed = max(time.perf_counter() - start, 1e-9)
    response.close()

    return total_bytes * 8 / elapsed / 1_000_000    

def test_github_profile_is_reachable():
    response = requests.request(method="GET", url=GITHUB_PROFILE_URL, timeout=10)
    assert response.status_code == 200


def test_download_speed_is_at_least_100_mbps():
    speed = measure_download_speed_mbps()
    print(f"\nMeasured download speed: {speed:.1f} Mbps")
    assert speed >= MIN_SPEED_MBPS, (
        f"Speed {speed:.1f} Mbps is below the {MIN_SPEED_MBPS} Mbps requirement"
    )