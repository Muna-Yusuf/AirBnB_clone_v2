#!/usr/bin/env bash
#Sets up your web servers for the deployment of web_static.

#Update and install nginx.
sudo apt-get -y update && sudo apt-get -y upgrade
sudo apt-get -y install nginx

#Creat folders "data, web_static, releases, shared, test"
sudo mkdir -p "/data/web_static/releases/test/"
sudo mkdir -p "/data/web_static/shared/"

#Creat html file && symbolic link(test, current)

contant="Holberton School"
html_content="<html>
  <head>
  </head>
  <body>
    $contant
  </body>
</html>"

echo "$html_content" | sudo tee /data/web_static/releases/test/index.html > /dev/null
rm -rf /data/web_static/current
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

#Give ownership of the /data/ folder to the ubuntu user AND group.
sudo chown -R ubuntu:ubuntu /data/

#Update the Nginx configuration.
sudo wget -q -o /etc/nginx/sites-available/default http://exampleconfig.com/static/raw/nginx/ubuntu20.04/etc/nginx/sites-available/default
config="/etc/nginx/sites-available/default"
echo "Holberton School Hello Worl" | sudo tee /var/www/html/index.html > /dev/null
sudo sed -i '/^}$/i \ \n\tlocation \/redirect_me {return 301 https:\/\/www.youtube.com\/watch?v=QH2-TGUlwu4;}' $config
sudo sed -i '/^}$/i \ \n\tlocation @404 {return 404 "Ceci n'\''est pas une page\\n";}' $config
sudo sed -i 's/=404/@404/g' $config
sudo sed -i "/^server {/a \ \tadd_header X-Served-By $HOSTNAME;" $config
sudo sed -i '/^server {/a \ \n\tlocation \/hbnb_static {alias /data/web_static/current/;index index.html;}' $config

#Restart Nginx
