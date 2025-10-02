"""
Show how many times each IP address accessed the webserver

Usage examples

- Show the current day's hits to brandonrohrer.com
    uv run ips

- Test against some stale data
    uv run ips.py --domain test

- Inspect the e2eml.school logs
    uv run ips.py --domain e2e

- Inspect the tyr.fyi logs
    uv run ips.py --domain tyr
"""

import argparse
import numpy as np
import log_reader

# domains = ["com", "com1", "e2e", "tyr", "def", "test"]


def show_ips(domain="com"):
    log_df = log_reader.get_logs(domain)
    ips = log_df["ip"].values
    ips, counts = np.unique(ips, return_counts=True)
    order = np.argsort(counts)
    for i in order:
        print(counts[i], ips[i])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--domain", default="com", required=False)
    args = parser.parse_args()

    show_ips(domain=args.domain)
