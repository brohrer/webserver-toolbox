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


## Update the allowlist of IP addresses

Update the contents of `~/webserver-tools/.allowlist.txt` to include
home IP.

Move it to a known location

`sudo mv .allowlist.txt /etc/nginx/`


## Auto-detect block-worthy IP addresses

`uv run autoblock.py`

for yesterday

`uv run autoblock.py -d com1`


## Update the virtual server (DigitalOcean droplet)

```
sudo apt update
sudo apt upgrade -y
```

## Cheatsheets

The copy/pastable cheatsheets by server are in 

- `doc/brandonrohrer.com.md`

## cron

[crontab debugging](https://stackoverflow.com/questions/22743548/cronjob-not-running)
