"""
run as

sudo python3 block_ips.py
"""
import os

blocklist = "blocklist.txt"

# load ip blocklist
with open(blocklist, "rt") as f:
    ips = f.readlines()

    for ip in ips:
        print(f"running: ufw insert 1 deny from {ip}")
        os.system(f"ufw insert 1 deny from {ip}")
