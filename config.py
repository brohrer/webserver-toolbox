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
test_log = "test.log"
