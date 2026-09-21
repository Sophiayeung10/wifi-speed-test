
# Wi-Fi PHY & Network Link Test Suite

An automated test suite designed to evaluate Wi-Fi network throughput and host reachability directly from a local test workstation. The project leverages `pytest` and `requests` to measure real-time download performance, enforcing a strict minimum threshold of 100 Mbps to validate network capability.

It also verifies basic internet connectivity by checking reachability to a designated host profile page.

## How it works

1. `requests.request("GET", ..., stream=True)` initiates a chunked download of a 50 MB payload hosted on Cloudflare's speed test server.
2. The script records the elapsed transfer time and calculates throughput in megabits per second (Mbps):
   `bytes x 8 / seconds / 1,000,000`
3. `assert speed >= 100` determines the test result (PASS / FAIL).
4. A 15-second timeout safeguard prevents persistent hanging on degraded or high-latency connections.

All execution logic is self-contained within `test_wifi.py` and run natively through `pytest`.

## Tests

| Test | What it checks |
|---|---|
| `test_github_profile_is_reachable` | Validates target URL (`https://github.com/Sophiayeung10`) returns an HTTP 200 OK status |
| `test_download_speed_is_at_least_100_mbps` | Asserts measured network download throughput meets or exceeds 100 Mbps |

## Requirements

- Python 3.10 or newer (validated on Python 3.14)
- `requests` and `pytest` dependencies

## Installation

```bash
git clone [https://github.com/Sophiayeung10/wifi-speed-test.git](https://github.com/Sophiayeung10/wifi-speed-test.git)
cd wifi-speed-test
python -m venv .venv
.venv\Scripts\activate        # macOS/Linux: source .venv/bin/activate
pip install requests pytest
```

##Usage
python -m pytest test_wifi.py -v -s
-v enables verbose output detailing individual test cases.

##Example output
test_wifi.py::test_github_profile_is_reachable PASSED
test_wifi.py::test_download_speed_is_at_least_100_mbps
Measured download speed: 338.8 Mbps
PASSED

2 passed in 2.16s

##Project Structure
```
wifi-speed-test/
  test_wifi.py        test cases and execution logic
  requirements.txt    project dependencies (requests, pytest)
  README.md           project documentation
  LICENSE             MIT license
  .gitignore          ignores virtual environments and build artifacts
-s prints stdout values (measured Mbps) directly to the console.
```
