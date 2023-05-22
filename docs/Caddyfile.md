#### About
##### Here you can find how to modify Caddy reverse proxy to use subdomain and subdirectory

##### Working solution
To get the Caddyfile configuration working following steps must be done:
 - resource files must use the correct subfolder.  
 For example in `analytics` module:
 index.html file should look like this
 ```
 <!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <link rel="icon" href="%PUBLIC_URL%/favicon.ico" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="description" content="Analytics Module" />
    <title>Bürokratt - Analytics Module</title>
<script defer src="/analytics/static/js/bundle.js"></script>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
  </body>
</html>
```

- Changing `Caddyfile` accordingly  
For example:  
```
admin.play.buerokratt.ee {

    handle_path /analytics/* {
        reverse_proxy * localhost:PORT_IP
        header Content-Type application/javascript
	}


log {
        output file /var/log/caddy/caddy.log
    }


}
```
