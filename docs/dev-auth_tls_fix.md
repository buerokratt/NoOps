#### How to skip self-signed certificate issue "Do you trust this page"  

To bypass this issue, you should add in Caddyfile `tls-veryfy-skip` line.  
For example:  
```
subdomain.example.ee {
        reverse_proxy * localhost:XXXX {
                transport http {
                        tls
                        tls_insecure_skip_verify
                }
                flush_interval 99
}
}
```

During the setup of login page, make sure, that the endpoint of `ruuter` is set using the DNS name and without the port.    
For example:  
```
RUUTER_API_URL: 'https://ruuter.example.ee',
```
