"""
Add new IP addresses to the blocklist, remove duplicates,
and sort the list.

Usage:
    uv run prepare_firewall_update.py

And follow up:
    sudo bash update_firewall.sh
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

    update(domain=args.domain, dryrun=args.dryrun, local=args.local)
