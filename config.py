"""
Some shared references across the library
"""

log_dir = "logs"

allowlist = "/etc/nginx/.allowlist.txt"
# For local testing
allowlist_local = ".allowlist.txt"

blocked_ips = "blocklist.txt"
ips_to_block = "blocklist_additions.txt"

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
    ".php",
    "wp-includes",
    "wp-content",
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
