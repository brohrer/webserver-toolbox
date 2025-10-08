"""
Comb the webserver's logs for block-worthy IP addresses.

Usage examples

- Comb the current day's hits to brandonrohrer.com
    uv run history.py

- Comb yesterday's hits to brandonrohrer.com
    uv run history.py --domain com1

- Test against some stale data
    uv run history.py --domain test
"""

import argparse
from datetime import datetime
import os
import config
import log_reader

# Attmepting to access files with these names even once will get a block
one_strike_pages = [
    ".env",
]

one_strike_actions = [
    "PROPFIND",
    "CONNECT",
]


def find_bad_behavior(domain="com", dryrun=False):
    """
    domain: str
        One of {"com", "com1", "e2e", "tyr", "def", "test"}.
        Specify which domain to show logs for, for example
        "com" = brandonrohrer.com, today
        "com1" = brandonrohrer.com, yesterday
        "test" = a test log for development
    """
    log_df = log_reader.get_logs(domain)

    # Check for one-strike-and-you're-out file access offenses
    one_strike_page_ips = []
    for i, row in log_df.iterrows():
        for part in row["uri"].split("/"):
            if part in one_strike_pages:
                one_strike_page_ips.append(row["ip"])

    # List each IP just once
    one_strike_ips = list(set(one_strike_page_ips))

    # Add these to the log

    isodate = datetime.now().isoformat().split("T")[0]
    log_filename = os.path.join(config.backup_dir, config.one_strike_page_log)
    with open(log_filename, "at") as f:
        for ip in one_strike_ips:
            if dryrun:
                print(f"adding {isodate} {ip} to the one-strike-page log")
            else:
                f.write(f"{isodate} {ip} \n")

    # Add these to the to-block list
    with open(config.ips_to_block, "at") as f:
        for ip in one_strike_ips:
            if dryrun:
                print(f"blocking {ip} as one-strike-page")
            else:
                f.write(ip + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--domain", default="com", required=False)
    parser.add_argument("-r", "--dryrun", action="store_true")
    args = parser.parse_args()
    find_bad_behavior(domain=args.domain, dryrun=args.dryrun)
