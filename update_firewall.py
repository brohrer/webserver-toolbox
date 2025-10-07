"""
Add new IP addresses to the blocklist, remove duplicates,
and sort the list.
"""
import os
import shutil
import time

allowlist = "/etc/nginx/.allowlist.txt"
# For local testing
# allowlist = ".allowlist.txt"

blocklist = "blocklist.txt"
new_ips = "blocklist_additions.txt"

backup_dir = "archive"

def main(dryrun=False):
    # backup blocklists
    shutil.copy(new_ips, os.path.join(backup_dir, new_ips + f".{int(time.time())}.bak"))
    try:
        shutil.copy(blocklist, os.path.join(backup_dir, blocklist + ".bak"))
    except FileNotFoundError:
        pass

    # load ip blocklist
    try:
        with open(blocklist, "rt") as f:
            blocklist_ips = list(f.readlines())
    except FileNotFoundError:
        blocklist_ips = []

    # load new ips to block
    with open(new_ips, "rt") as f:
        new_block_ips = list(f.readlines())

    # load new ips to block
    with open(allowlist, "rt") as f:
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
    with open(blocklist, "wt") as f:
        for ip in block_ips:
            f.write(ip + "\n")

    # reset an empty list of ips to add to the blocklist
    with open(new_ips, "wt") as f:
        f.write("# IP addresses to be added to the blocklist\n")

    for ip in block_ips:
        print(f"running: ufw insert 1 deny from {ip}")
        os.system(f"ufw insert 1 deny from {ip}")

    for ip in allow_ips:
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
        int(parts[0]) * 1_000_000_000 +
        int(parts[1]) * 1_000_000 +
        int(parts[2]) * 1000 +
        int(parts[3])
    )
    return key


if __name__ == "__main__":
    main(dryrun=True)
