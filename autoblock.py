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
import reader

# Attmepting to access files with these names even once will get a block
one_strike_pages = [
    ".env",
]

n_strikes = 5
n_strike_pages = [
    ".php",
    "wp-includes",
]

one_strike_actions = [
    "CONNECT",
    "PROPFIND",
    "SSTP_DUPLEX_POST",
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
    log_df = reader.get_logs(domain)

    _scan_for_one_strike_page_violations(log_df, dryrun)
    _scan_for_n_strike_page_violations(log_df, dryrun)
    _scan_for_one_strike_action_violations(log_df, dryrun)


def _scan_for_one_strike_page_violations(log_df, dryrun):
    # Check for one-strike-and-you're-out file access offenses
    one_strike_page_ips = []
    for i, row in log_df.iterrows():
        for part in row["uri"].split("/"):
            if part in one_strike_pages:
                one_strike_page_ips.append(row["ip"])

    # List each IP just once
    one_strike_page_ips = list(set(one_strike_page_ips))

    # Add these to the log
    isodate = datetime.now().isoformat().split("T")[0]
    log_filename = os.path.join(config.log_dir, config.one_strike_page_log)
    with open(log_filename, "at") as f:
        for ip in one_strike_page_ips:
            if dryrun:
                print(f"adding {isodate} {ip} to the one-strike-page log")
            else:
                f.write(f"{isodate} {ip} \n")

    # Add these to the to-block list
    with open(config.ips_to_block, "at") as f:
        for ip in one_strike_page_ips:
            if dryrun:
                print(f"blocking {ip} as one-strike-page")
            else:
                f.write(ip + "\n")


def _scan_for_n_strike_page_violations(log_df, dryrun):
    # Check for three-strikes-and-you're-out file access offenses
    # These are more annoyances than direct attacks
    strikes = {}
    for i, row in log_df.iterrows():
        for page in n_strike_pages:
            if page in row["uri"]:
                if row["ip"] in strikes:
                    strikes[row["ip"]] += 1
                else:
                    strikes[row["ip"]] = 1

    n_strike_page_ips = []
    for ip, strike_count in strikes.items():
        if strike_count >= n_strikes:
            n_strike_page_ips.append(ip)

    # List each IP just once
    n_strike_page_ips = list(set(n_strike_page_ips))

    # Add these to the log
    isodate = datetime.now().isoformat().split("T")[0]
    log_filename = os.path.join(config.log_dir, config.n_strike_page_log)
    with open(log_filename, "at") as f:
        for ip in n_strike_page_ips:
            if dryrun:
                print(f"adding {isodate} {ip} to the n-strike-page log")
            else:
                f.write(f"{isodate} {ip} \n")

    # Add these to the to-block list
    with open(config.ips_to_block, "at") as f:
        for ip in n_strike_page_ips:
            if dryrun:
                print(f"blocking {ip} as n-strike-page")
            else:
                f.write(ip + "\n")


def _scan_for_one_strike_action_violations(log_df, dryrun):
    # Check for one-strike-and-you're-out attempted action offenses
    one_strike_action_ips = []
    for i, row in log_df.iterrows():
        if row["action"] in one_strike_actions:
            one_strike_action_ips.append(row["ip"])

    # List each IP just once
    one_strike_action_ips = list(set(one_strike_action_ips))

    # Add these to the log
    isodate = datetime.now().isoformat().split("T")[0]
    log_filename = os.path.join(config.log_dir, config.one_strike_action_log)
    with open(log_filename, "at") as f:
        for ip in one_strike_action_ips:
            if dryrun:
                print(f"adding {isodate} {ip} to the one-strike-action log")
            else:
                f.write(f"{isodate} {ip} \n")

    # Add these to the to-block list
    with open(config.ips_to_block, "at") as f:
        for ip in one_strike_action_ips:
            if dryrun:
                print(f"blocking {ip} as one-strike-action")
            else:
                f.write(ip + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--domain", default="com", required=False)
    parser.add_argument("-r", "--dryrun", action="store_true")
    args = parser.parse_args()
    find_bad_behavior(domain=args.domain, dryrun=args.dryrun)
