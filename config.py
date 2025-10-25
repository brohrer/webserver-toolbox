"""
Some shared references across the library
"""

import os
from pathlib import Path

module_path = os.path.abspath(__file__)
module_dir = Path(module_path).parent

log_dir_name = "logs"
log_dir = module_dir.joinpath(log_dir_name)

firewall_update_script = "update_firewall.sh"

allowlist = "/etc/nginx/.allowlist.txt"
# For local testing
allowlist_local = ".allowlist.txt"

blocked_ips_filename = "blocklist.txt"
blocked_ips = module_dir.joinpath(blocked_ips_filename)
ips_to_block_filename = "blocklist_additions.txt"
ips_to_block = module_dir.joinpath(ips_to_block_filename)

one_strike_action_log = "blocks_one_strike_action.txt"
one_strike_page_log = "blocks_one_strike_page.txt"
n_strike_page_log = "blocks_n_strike_page.txt"
n_strike_action_log = "blocks_n_strike_action.txt"
n_strike_status_log = "blocks_n_strike_status.txt"
test_log = "test.log"

# Attmepting to access files with these names even once will get a block
one_strike_pages = [
    ".env",
]

n_strikes_for_pages = 5
n_strike_pages = [
    ".7z",
    ".gz",
    ".php",
    ".rar",
    "wp-includes",
    "wp-content",
    ".zip"
]

one_strike_actions = [
    "CONNECT",
    "PROPFIND",
    "SSTP_DUPLEX_POST",
]

n_strikes_for_actions = 8
n_strike_actions = [
    "",  # missing action
    "POST",
]

n_strikes_for_status = 8
n_strike_status = [
    "403",
    "404",
    "429",
]
