# Maintenance tasks for `brandonrohrer.com`

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

## Update the virtual server (DigitalOcean droplet)

```
sudo apt update
sudo apt upgrade -y
```
