#### About  
Here is writte, how to create self-signed certificates and Certification Authoroty  

##### Generating a Certificate Signing Request (CSR)
Create the CSR, do not leave passhprase empty for security reasons  
IMPORTANT!!!   
Make sure to store the passphrased used.


` openssl genrsa -des3 -out server.key 2048 `  

Create the insecure key, the one without a passphrase, and shuffle the key names

`openssl rsa -in server.key -out server.key.insecure`  

`mv server.key server.key.secure`
`mv server.key.insecure server.key`  

##### The insecure key is now named server.key, and you can use this file to generate the CSR without passphrase.  

Create CSR

`openssl req -new -key server.key -out server.csr`  

Create selfsigned certificate

`openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt`  

Install the key file server.key and certificate file server.crt

`sudo cp server.crt /etc/ssl/certs`  
`sudo cp server.key /etc/ssl/private`
