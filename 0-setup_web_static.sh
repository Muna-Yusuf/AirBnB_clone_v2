#!/usr/bin/env bash
#Sets up your web servers for the deployment of web_static.

#Update and install nginx.
apt-get -y update && sudo apt-get -y upgrade
apt-get -y install nginx

#Creat folders "data, web_static, releases, shared, test"
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

#Creat html file && symbolic link(test, current)
echo "testing Nginx configuration" > /data/web_static/releases/test/index.html
ln -sf /data/web_static/releases/test/ /data/web_static/current

#Give ownership of the /data/ folder to the ubuntu user AND group.
chown -R ubuntu /data/
chgrp -R ubuntu /data/

#Update the Nginx configuration.
printf %s "server{
	listen 80 defualut_server;
	add_header X-served-By $hostname;
	root  /var/www/html;
	index index.html index.html;
	
	location /hbnb_static {
	alias /data/web_static/current/;
	index index.html index.html;
	}

	location /redirect_me {
	return 301 https://github.com/Muna-Yusuf; 
	}

	error_page 404 /404.html;

	location /404 {
	root /var/www/html;
	internal;
	}
}" > /etc/nginx/sites-available/default

#Restart Nginx
service nginx restart
