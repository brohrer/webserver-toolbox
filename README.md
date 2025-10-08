# webserver-toolbox

## Log inspection

`uv run history.py` to browse the day's history

`uv run pages.py` to browse the day's most popular pages

`uv run ips.py` to browse the day's most active IP addresses

Browse the files for more options

## Update the blocklist

Add any IP addresses from `blocklist_additions.txt` to the running
blocklist.

`sudo /home/$USER/.local/bin/uv run update_firewall.py`

or

`sudo python3 update_firewall.py`

## Cheatsheets

The copy/pastable cheatsheets by server are in 

- `doc/brandonrohrer.com.md`
