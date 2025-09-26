## Deploy the server block files

After every nginx change

```
sudo nginx -t
sudo systemctl restart nginx
```

Update the server block on the DigitalOcean server droplet

```
sudo cp /etc/nginx/sites-available/brandonrohrer.com /etc/nginx/sites-available/brandonrohrer.com.bak
sudo cp ~/webeserver-toolbox/server_blocks/brandonrohrer.com /etc/nginx/sites-available/brandonrohrer.com
```
