#### About
##### Here is shown nginx configuration sample on how to guide traffic between containers. 


##### Traffic between Pubic ruuter v1 and v2 + reverse proxy 
Conf file is stored:
`/etc/nginx/conf.d`

```
server {
    listen 80;
#    access_log  /var/log/nginx/api.log; ## add where logs are stored
#    error_log   /var/log/nginx/api_error.log; ## add where logs are stored
    server_name ruuter.test.buerokratt.ee;

    location /v2/ {

            rewrite ^/v2/?(.*) /$1 break;
            proxy_pass         http://x.x.x.x:8080/;
            proxy_redirect     off;
            proxy_set_header   Host $host;
            proxy_set_header   X-Real-IP $remote_addr;
            proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header   X-Forwarded-Host $server_name;
    }

    location /v1/ {

            rewrite ^/v1/?(.*) /$1 break;
            proxy_pass         https://x.x.x.x:8091/;
            proxy_redirect     off;
            proxy_set_header   Host $host;
            proxy_set_header   X-Real-IP $remote_addr;
            proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header   X-Forwarded-Host $server_name;
    }
}
```

##### Important  

In `/etc/nginx/nginx.conf` check if:
```
include /etc/nginx/conf.d/*.conf;
```
is present. If not add it, otherwise it wont be loaded as part of the nginx reverse proxy

Example:

```
http {

	##
	# Basic Settings
	##

	sendfile on;
	tcp_nopush on;
	tcp_nodelay on;
	keepalive_timeout 65;
	types_hash_max_size 2048;
	# server_tokens off;
        expires off;

	# server_names_hash_bucket_size 64;
	# server_name_in_redirect off;

	include /etc/nginx/mime.types;
	default_type application/octet-stream;

	##
	# SSL Settings
	##

	ssl_protocols TLSv1.3; # Dropping SSLv3, ref: POODLE
	#ssl_protocols TLSv1 TLSv1.1 TLSv1.2 TLSv1.3; # Dropping SSLv3, ref: POODLE
	ssl_prefer_server_ciphers on;

	##
	# Logging Settings
	##

	access_log /var/log/nginx/access.log;
	error_log /var/log/nginx/error.log;

	##
	# Gzip Settings
	##

	gzip on;

	# gzip_vary on;
	# gzip_proxied any;
	# gzip_comp_level 6;
	# gzip_buffers 16 8k;
	# gzip_http_version 1.1;
	# gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

	##
	# Virtual Host Configs
	##

	include /etc/nginx/conf.d/*.conf;
#	include /etc/nginx/sites-availabe/*;
}
```
#### Note  
You can create a conf file for every service, nginx.conf will load them due to `include /etc/nginx/conf.d/*.conf;`
