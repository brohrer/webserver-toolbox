"""
Show the webserver's logs in an easier to read format.

Usage examples

- Show the current day's hits to brandonrohrer.com
    uv run history.py

- Show the hits from a particular IP address
    uv run history.py --ip 123.123.123.123

- Test against some stale data
    uv run history.py --domain test

- Inspect the e2eml.school logs
    uv run history.py --domain e2e

- Inspect the tyr.fyi logs
    uv run history.py --domain tyr


`targets_to_ignore` is a list of URLs that are uninteresting
and shouldn't be displayed.
"""

import argparse
from targets import targets_to_ignore
import log_reader

# domains = ["com", "com1", "e2e", "tyr", "def", "test"]


def show_history(domain="com", ip=None, status=None):
    log_df = log_reader.get_logs(domain)
    for i, row in log_df.iterrows():
        if ip is not None:
            if row["ip"] != ip:
                continue
        if status is not None:
            if row["code"] != status:
                continue
        # Ignore some common ones
        if row["uri"] not in targets_to_ignore:
            print(
                f"{row['hour']}:{row['minute']}:{row['second']}  "
                + f"{row['action']} "
                + f"{row['code']} "
                + f"{row['ip']} "
                + f"{row['uri']}"
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--domain", default="com", required=False)
    parser.add_argument("--ip", default=None)
    parser.add_argument("-s", "--status", default=None)
    args = parser.parse_args()

    show_history(domain=args.domain, ip=args.ip, status=args.status)
