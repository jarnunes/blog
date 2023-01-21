## Basis System Configuration

1. First, we need update the SO. Run the commands below:

> sudo apt update & sudo apt upgrade

2. Now, install the libraries:

> sudo apt install libpq-dev python3-dev

> sudo apt install python3-pip

> sudo apt install nginx

> python3 -m pip install --upgrade pip

> sudo apt install python3.10-venv

3. And finally, clone the project on git repository:

> git clone https://github.com/jarnunes/blog.git

4. Navigate into the project folder and create the virtual env

> python3 -m venv venv

5. Now, activate the env:

> source venv/bin/activate

5.1 To deactivate, run: ``deactivate``

6. Install all requirements for your project. 
7. For test:
> python3 manage.py migrate

> python3 manage.py collectstatic

> python3 manage.py runserver 0.0.0.0:8000

> gunicorn --bind 0.0.0.0:8000 core.wsgi

Access your application and check if it's ok. 

## Configure Nginx and Gunicorn

The article reference are available on this [Link](https://www.codewithharry.com/blogpost/django-deploy-nginx-gunicorn/)

1. Create the file gunicorn.socket

> sudo nano /etc/systemd/system/gunicorn.socket

2. Now, past the content:

```shell
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```

3. Create the blog.service with command:

> sudo nano /etc/systemd/system/gunicorn.service

4. And past the file content bellow. Pay attention here: You need replace the ``WorkingDirectory`` value with your
   project home directory.
   After, replace ``ExecStart`` with your project home directory, including ``/venv/bin/gunicorn``.
   And finally, ``core.wsgi:application`` needs replaced with your_project_core.wsgi:application.

```shell
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/blog
ExecStart=/home/ubuntu/blog/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          core.wsgi:application

[Install]
WantedBy=multi-user.target
```

5. Now, we need activate the socket.
> sudo systemctl start gunicorn.socket

> sudo systemctl enable gunicorn.socket

> sudo systemctl status gunicorn.socket
6. For check if it's ok, run:
> sudo systemctl status gunicorn.socket

> sudo systemctl status gunicorn

> curl --unix-socket /run/gunicorn.sock localhost

> sudo systemctl status gunicorn

7. Now, we're going to configure nginx:
> sudo nano /etc/nginx/sites-available/blog
```shell
server {
    listen 80;
    server_name localhost;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        root /home/ubuntu/blog;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```

8. Copy the created file to sites-enabled folder with command:
> sudo ln -s /etc/nginx/sites-available/blog /etc/nginx/sites-enabled/

9. Finally, remove the default nginx site and check configuration:
> sudo rm /etc/nginx/sites-enabled/default

> sudo systemctl restart nginx

> sudo systemctl restart gunicorn

# Configuring SSL
```shell
sudo openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048
sudo apt-get install certbot
sudo service nginx stop
sudo certbot certonly --standalone -d your-domain.com
sudo service nginx start
```

Now, you need replace your nginx configuration for accept SSL connections:
> sudo nano /etc/nginx/sites-available/blog
````shell
server {
	listen 80;
	listen [::]:80;

	listen 443 ssl http2;
	listen [::]:443 ssl http2;
	ssl_certificate /etc/letsencrypt/live/blog.jnunesc.com.br/fullchain.pem; # managed by Certbot
	ssl_certificate_key /etc/letsencrypt/live/blog.jnunesc.com.br/privkey.pem; # managed by Certbot
	ssl_trusted_certificate /etc/letsencrypt/live/blog.jnunesc.com.br/chain.pem;

	# Improve HTTPS performance with session resumption
	ssl_session_cache shared:SSL:10m;
	ssl_session_timeout 5m;

	# Enable server-side protection against BEAST attacks
	ssl_prefer_server_ciphers on;
	ssl_ciphers ECDH+AESGCM:ECDH+AES256:ECDH+AES128:DH+3DES:!ADH:!AECDH:!MD5;

	# Disable SSLv3
	ssl_protocols TLSv1 TLSv1.1 TLSv1.2;

	# Diffie-Hellman parameter for DHE ciphersuites
	# $ sudo openssl dhparam -out /etc/ssl/certs/dhparam.pem 4096
	ssl_dhparam /etc/ssl/certs/dhparam.pem;

	# Enable HSTS (https://developer.mozilla.org/en-US/docs/Security/HTTP_Strict_Transport_Security)
	add_header Strict-Transport-Security "max-age=63072000; includeSubdomains";

	# Enable OCSP stapling (http://blog.mozilla.org/security/2013/07/29/ocsp-stapling-in-firefox)
	ssl_stapling on;
	ssl_stapling_verify on;
	resolver 8.8.8.8 8.8.4.4 valid=300s;
	resolver_timeout 5s;

	# Add index.php to the list if you are using PHP
	index index.html index.htm index.nginx-debian.html index.php;

	server_name blog2.jnunesc.com.br;

	location = /favicon.ico { access_log off; log_not_found off; }
	location /static/ {
			root /home/ubuntu/blog;
	}

	location /media {
			alias /home/ubuntu/blog/media/;
	}

	location / {
			include proxy_params;
			proxy_pass http://unix:/run/gunicorn.sock;
	}

	# deny access to .htaccess files, if Apache's document root
	# concurs with nginx's one
	#
	location ~ /\.ht {
		deny all;
	}

	location ~ /\. {
		access_log off;
		log_not_found off;
		deny all;
	}

	gzip on;
	gzip_disable "msie6";

	gzip_comp_level 6;
	gzip_min_length 1100;
	gzip_buffers 4 32k;
	gzip_proxied any;
	gzip_types
		text/plain
		text/css
		text/js
		text/xml
		text/javascript
		application/javascript
		application/x-javascript
		application/json
		application/xml
		application/rss+xml
		image/svg+xml;

  access_log off;
	access_log  /var/log/nginx/blog.jnunesc.com.br-access.log;
	error_log   /var/log/nginx/blog.jnunesc.com.br-error.log;

	include /etc/nginx/common/protect.conf;
}

````
> sudo systemctl restart nginx

> sudo systemctl restart gunicorn


## Commons errors

#### 403 Forbidden
this error can occur when accessing static files (css, js).
For more details, access this [link](https://stackoverflow.com/questions/16808813/nginx-serve-static-file-and-got-403-forbidden)
```shell
  sudo usermod -a -G your_user www-data

  sudo chown -R :www-data /path/to/your/static/folder
  sudo chown -R :www-data /path/to/your/media/folder
```