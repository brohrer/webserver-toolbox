# webserver-toolbox

This package has a collection of tools I've found helpful in deploying
and maintaining a static website, which I use to host my blog.
Accompanying posts [on the blog](https://brandonrohrer.com):
[I](https://brandonrohrer.com/hosting.html),
[II](https://brandonrohrer.com/hosting2.html),
[III](https://brandonrohrer.com/hosting3.html),
[IV](https://brandonrohrer.com/hosting4.html),
[V](https://brandonrohrer.com/hosting5.html),
[VI](https://brandonrohrer.com/hosting6.html),
[VII](https://brandonrohrer.com/hosting7.html)


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


## Set up a recurring task with `cron`


[crontab debugging](https://stackoverflow.com/questions/22743548/cronjob-not-running)


## Restart nginx

After every nginx change

```
sudo nginx -t
sudo systemctl restart nginx
```

