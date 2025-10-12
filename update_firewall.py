"""
Add new IP addresses to the blocklist, remove duplicates,
and sort the list.

Usage:
    sudo /home/$USER/.local/bin/uv run update_firewall.py
or
    sudo python3 update_firewall.py
"""

import argparse
import os
import shutil
import time
import config


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
        new_block_ips = list(f.readlines())

    # load new ips to block
    if local:
        with open(config.allowlist_local, "rt") as f:
            allowlist_ips = list(f.readlines())
    else:
        with open(config.allowlist, "rt") as f:
            allowlist_ips = list(f.readlines())

    block_ips = []
    for ip in blocklist_ips + new_block_ips:
        ip = ip.strip()
        if is_valid_ip(ip):
            block_ips.append(ip)

    # Ensure each IP address only shows up once
    block_ips = list(set(block_ips))

    # Sort ips numerically by address fields
    block_ips.sort(key=ip_to_key)

    allow_ips = []
    for ip in allowlist_ips:
        ip = ip.strip()
        if is_valid_ip(ip):
            allow_ips.append(ip)

    # write updated ip blocklist
    if dryrun:
        for ip in block_ips:
            print(f"dryrun: writing {ip} to blocklist")
    else:
        with open(config.blocked_ips, "wt") as f:
            for ip in block_ips:
                f.write(ip + "\n")

    # reset an empty list of ips to add to the blocklist
    if not dryrun:
        with open(config.ips_to_block, "wt") as f:
            f.write("# IP addresses to be added to the blocklist\n")

    for ip in block_ips:
        if dryrun:
            print(f"dryrun: ufw insert 1 deny from {ip}")
        else:
            print(f"running: ufw insert 1 deny from {ip}")
            os.system(f"ufw insert 1 deny from {ip}")

    for ip in allow_ips:
        if dryrun:
            print(f"dryrun: ufw insert 1 allow from {ip}")
        else:
            print(f"running: ufw insert 1 allow from {ip}")
            os.system(f"ufw insert 1 allow from {ip}")


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

    update(domain=args.domain, dryrun=args.dryrun, local=args.local)
