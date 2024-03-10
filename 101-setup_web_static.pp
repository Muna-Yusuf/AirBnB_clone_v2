# Redo task 0 using puppet

exec { 'updata':
  command => '/usr/bin/apt-get update',
}

-> package { 'nginx':
  ensure => installed,
}

-> exec { 'mkdir':
  command => "/usr/bin/mkdir -p '/data/web_static/releases/test/' '/data/web_static/shared/'"
}

-> exec { 'simple content':
  command => '/usr/bin/echo "simple content!" | sudo tee /data/web_static/releases/test/index.html > /dev/null',
}
-> exec { 'rm':
  command => '/usr/bin/rm -rf /data/web_static/current',
}
-> exec { 'symbolic link':
  command => '/usr/bin/ln -s /data/web_static/releases/test/ /data/web_static/current',
}
-> exec { 'chown':
  command => '/usr/bin/chown -R ubuntu:ubuntu /data/',
}
-> exec { 'hbnb_static':
  command => 'sudo sed -i "/^server {/a \ \n\tlocation \/hbnb_static {alias /data/web_static/current/; index index.html;}" /etc/nginx/sites-enabled/default',
  provider => shell,
}
-> exec { 'restart nginx':
  command => '/usr/sbin/service nginx restart',
}
