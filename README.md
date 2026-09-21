# Wifi speed test for my GitHub portfolio

I want to create an automated test. When I go to my GitHub public profile page, I want to test my Wi-Fi speed at that time. If the speed is lower than 100 Mbps, the test should fail. This project does not use `run_tests.py` because there is no physical equipment connected. The test checks my internet download speed using `pytest` and `requests`(`requests.request()` = calls the `request` function from the `requests` library.).

It also checks that my GitHub profile page is reachable.

## How it works

1. `requests.request("GET", ..., stream=True)` starts downloading a 50 MB test file from Cloudflare's speed test server.
2. The script times the download and converts it to megabits per second (Mbps):
   `bytes x 8 / seconds / 1,000,000`
3. `assert speed >= 100` decides PASS or FAIL.
4. If the connection is very slow, the download stops after 15 seconds so the test never hangs.

No separate program file is needed: `test_wifi.py` calls `requests` directly and pytest runs it.

## Tests

| Test | What it checks |
|---|---|
| `test_github_profile_is_reachable` | `https://github.com/Sophiayeung10` responds with HTTP status 200 |
| `test_download_speed_is_at_least_100_mbps` | Measured download speed is at least 100 Mbps |

## Requirements

- Python 3.10 or newer (tested on Python 3.14)
- `requests` and `pytest` (installed in the steps below)

## Installation

```bash
git clone https://github.com/Sophiayeung10/wifi-speed-test.git
cd wifi-speed-test
python -m venv .venv
.venv\Scripts\activate        # macOS/Linux: source .venv/bin/activate
pip install requests pytest
```

## Usage

```bash
python -m pytest test_wifi.py -v -s
```

- `-v` shows each test name.
- `-s` shows the printed speed value.

### Example output

Speed measured on my home connection:

```
test_wifi.py::test_github_profile_is_reachable PASSED
test_wifi.py::test_download_speed_is_at_least_100_mbps
Measured download speed: 338.8 Mbps
PASSED

2 passed in 2.16s
```

## Configuration

Edit the constants at the top of `test_wifi.py`:

| Constant | Meaning | Default |
|---|---|---|
| `MIN_SPEED_MBPS` | Minimum speed required to pass | `100` |
| `MAX_TEST_SECONDS` | Stop the download after this many seconds | `15` |
| `SPEED_TEST_URL` | File that is downloaded | Cloudflare 50 MB test file |
| `GITHUB_PROFILE_URL` | Page used for the reachability check | My GitHub profile |

## Notes and limitations

- This measures download speed from this computer to the internet. It is not the raw Wi-Fi link speed between the device and the router.
- Results change with the time of day, distance from the router, and other devices using the network.
- A single-connection test can under-report on very fast lines, so treat the result as a rough check and run it more than once before drawing conclusions.
- Do not run this in GitHub Actions or other cloud CI. It would measure the cloud server's network, not my Wi-Fi.

## Project structure
```
wifi-speed-test/
  test_wifi.py        the tests
  requirements.txt    libraries needed to run them (requests, pytest)
  README.md           this file
  LICENSE             MIT license
  .gitignore          keeps .venv and cache folders out of Git
```

## Ideas for improvement

- Save each result with a timestamp to a CSV file to compare speeds at different times of day.
- Pass the minimum speed on the command line instead of editing the file.
- Add an upload speed test.
- Compare Wi-Fi against a wired connection.

## License

MIT