# Maintenance tasks for `brandonrohrer.com`


## Deploy content updates from local box to git repositories

- If authoring a new page, `page.md`, in `brandonrohrer.com/markdown`
run `uv run converter.py page.md`
- In browser open up `page.html` and inspect.
- `git status`
- `git add page.html page.md` and any other files that need adding
- `git commit -m "commit message"`
- `git push codeberg HEAD`
- `git push github HEAD`
- `git push gitlab HEAD`

## Deploy content updates from git repositories to webserver

- `ssh blog`
- `cd /var/www/brandonrohrer.com/`
- `sudo git pull origin HEAD`

## Make a change to the server block

Re-deploy the server block files on the DigitalOcean server droplet.
First make a backup of the existing server block file.
Then update the server block.

```
sudo cp /etc/nginx/sites-available/brandonrohrer.com /etc/nginx/sites-available/brandonrohrer.com.bak
sudo cp ~/webserver-toolbox/server_blocks/brandonrohrer.com /etc/nginx/sites-available/brandonrohrer.com
```

After every nginx change

```
sudo nginx -t
sudo systemctl restart nginx
```

