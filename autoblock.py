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
import shutil
import time
import config
import reader

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
    _scan_for_n_strike_action_violations(log_df, dryrun)
    _scan_for_n_strike_status_violations(log_df, dryrun)


def _scan_for_one_strike_page_violations(log_df, dryrun):
    # Check for one-strike-and-you're-out file access offenses
    one_strike_page_ips = []
    for i, row in log_df.iterrows():
        for part in row["uri"].split("/"):
            if part in config.one_strike_pages:
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
        for page in config.n_strike_pages:
            if page in row["uri"]:
                if row["ip"] in strikes:
                    strikes[row["ip"]] += 1
                else:
                    strikes[row["ip"]] = 1

    n_strike_page_ips = []
    for ip, strike_count in strikes.items():
        if strike_count >= config.n_strikes_for_pages:
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
        if row["action"] in config.one_strike_actions:
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


def _scan_for_n_strike_action_violations(log_df, dryrun):
    # Check for three-strikes-and-you're-out file access offenses
    # These are more annoyances than direct attacks
    strikes = {}
    for i, row in log_df.iterrows():
        for action in config.n_strike_actions:
            if action == row["action"]:
                if row["ip"] in strikes:
                    strikes[row["ip"]] += 1
                else:
                    strikes[row["ip"]] = 1

    n_strike_action_ips = []
    for ip, strike_count in strikes.items():
        if strike_count >= config.n_strikes_for_actions:
            n_strike_action_ips.append(ip)

    # List each IP just once
    n_strike_action_ips = list(set(n_strike_action_ips))

    # Add these to the log
    isodate = datetime.now().isoformat().split("T")[0]
    log_filename = os.path.join(config.log_dir, config.n_strike_action_log)
    with open(log_filename, "at") as f:
        for ip in n_strike_action_ips:
            if dryrun:
                print(f"adding {isodate} {ip} to the n-strike-action log")
            else:
                f.write(f"{isodate} {ip} \n")

    # Add these to the to-block list
    with open(config.ips_to_block, "at") as f:
        for ip in n_strike_action_ips:
            if dryrun:
                print(f"blocking {ip} as n-strike-action")
            else:
                f.write(ip + "\n")


def _scan_for_n_strike_status_violations(log_df, dryrun):
    # Check for three-strikes-and-you're-out file access offenses
    # These are more annoyances than direct attacks
    strikes = {}
    for i, row in log_df.iterrows():
        for status in config.n_strike_status:
            if status == row["code"]:
                if row["ip"] in strikes:
                    strikes[row["ip"]] += 1
                else:
                    strikes[row["ip"]] = 1

    n_strike_status_ips = []
    for ip, strike_count in strikes.items():
        if strike_count >= config.n_strikes_for_status:
            n_strike_status_ips.append(ip)

    # List each IP just once
    n_strike_status_ips = list(set(n_strike_status_ips))

    # Add these to the log
    isodate = datetime.now().isoformat().split("T")[0]
    log_filename = os.path.join(config.log_dir, config.n_strike_status_log)
    with open(log_filename, "at") as f:
        for ip in n_strike_status_ips:
            if dryrun:
                print(f"adding {isodate} {ip} to the n-strike-status log")
            else:
                f.write(f"{isodate} {ip} \n")

    # Add these to the to-block list
    with open(config.ips_to_block, "at") as f:
        for ip in n_strike_status_ips:
            if dryrun:
                print(f"blocking {ip} as n-strike-status")
            else:
                f.write(ip + "\n")


def update(domain="com", dryrun=False, local=False):
    # backup blocklists
    source = config.ips_to_block
    backup_filename = config.ips_to_block_filename + f".{int(time.time())}.bak"
    target = config.log_dir.joinpath(backup_filename)
    if dryrun:
        print(f"Dryrun: Copying {source} to {target}")
    else:
        shutil.copy(source, target)
    try:
        source = config.blocked_ips
        backup_filename = config.blocked_ips_filename + ".bak"
        target = config.log_dir.joinpath(backup_filename)

        if dryrun:
            print(f"Dryrun: Copying {source} to {target}")
        else:
            shutil.copy(source, target)

    except FileNotFoundError:
        pass

    # load ip blocklist
    try:
        with open(config.blocked_ips, "rt") as f:
            blocklist_ips = list(f.readlines())
    except FileNotFoundError:
        blocklist_ips = []

    # load new ips to block
    with open(config.ips_to_block, "rt") as f:
        new_block_ips_raw = list(f.readlines())

    # load new ips to block
    if local:
        with open(config.allowlist_local, "rt") as f:
            allowlist_ips = list(f.readlines())
    else:
        with open(config.allowlist, "rt") as f:
            allowlist_ips = list(f.readlines())

    new_block_ips = []
    for ip in new_block_ips_raw:
        ip = ip.strip()
        if is_valid_ip(ip):
            new_block_ips.append(ip)

    updated_blocklist = []
    for ip in blocklist_ips + new_block_ips:
        ip = ip.strip()
        if is_valid_ip(ip):
            updated_blocklist.append(ip)

    # Ensure each IP address only shows up once
    updated_blocklist = list(set(updated_blocklist))

    # Sort ips numerically by address fields
    updated_blocklist.sort(key=ip_to_key)

    allow_ips = []
    for ip in allowlist_ips:
        ip = ip.strip()
        if is_valid_ip(ip):
            allow_ips.append(ip)

    # reset an empty list of ips to add to the blocklist
    if not dryrun:
        with open(config.ips_to_block, "wt") as f:
            f.write("# IP addresses to be added to the blocklist\n")

        try:
            os.remove(config.firewall_update_script)
        except FileNotFoundError:
            pass

    # refresh the allowlisted ips
    for ip in allow_ips:
        rule = f"ufw insert 1 allow from {ip}"
        if dryrun:
            print(f"dryrun: {rule}")
        else:
            with open(config.firewall_update_script, "at") as f:
                f.write(f"echo '{rule}'\n")
                f.write(f"{rule}\n")

    # block any newly added ips
    insert_position = len(allow_ips) + 1
    for ip in new_block_ips:
        rule = f"ufw insert {insert_position} deny from {ip}"
        if dryrun:
            print(f"dryrun: {rule}")
        else:
            with open(config.firewall_update_script, "at") as f:
                f.write(f"echo '{rule}'\n")
                f.write(f"{rule}\n")

    # write updated ip blocklist
    if dryrun:
        for ip in updated_blocklist:
            print(f"dryrun: writing {ip} to blocklist")
    else:
        with open(config.blocked_ips, "wt") as f:
            for ip in updated_blocklist:
                f.write(ip + "\n")


def is_valid_ip(ip):
    """
    Check whether there are four fields separated by a period
    and whether each of those is an integer between 0 and 255
    """
    parts = ip.split(".")
    if len(parts) != 4:
        return False
    for part in parts:
        try:
            if (int(part) < 0) or (int(part) > 255):
                return False
        except ValueError:
            return False
    return True


def ip_to_key(ip):
    parts = ip.split(".")
    key = (
        int(parts[0]) * 1_000_000_000
        + int(parts[1]) * 1_000_000
        + int(parts[2]) * 1000
        + int(parts[3])
    )
    return key


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--domain", default="com", required=False)
    parser.add_argument("-r", "--dryrun", action="store_true")
    parser.add_argument("-l", "--local", action="store_true")
    args = parser.parse_args()

    find_bad_behavior(domain=args.domain, dryrun=args.dryrun)
    update(domain=args.domain, dryrun=args.dryrun, local=args.local)
