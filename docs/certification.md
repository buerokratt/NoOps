#### About  
Here is writte, how to create self-signed certificates and Certification Authoroty  

##### Generating a Certificate Signing Request (CSR)
Create the CSR, do not leave passhprase empty for security reasons  
IMPORTANT!!!   
Make sure to store the passphrased used.



Create the insecure key, the one without a passphrase, and shuffle the key names

```openssl rsa -in server.key -out server.key.insecure```

```mv server.key server.key.secure```
```mv server.key.insecure server.key```  

##### The insecure key is now named server.key, and you can use this file to generate the CSR without passphrase.  

Create CSR

```openssl req -new -key server.key -out server.csr```  

Create selfsigned certificate

```openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt```  

Install the key file server.key and certificate file server.crt

```sudo cp server.crt /etc/ssl/certs```  
```sudo cp server.key /etc/ssl/private```

##### Certification Authority  

Create the directories to hold the CA certificate and related files

```sudo mkdir /etc/ssl/CA```  
```sudo mkdir /etc/ssl/newcerts```  

The CA needs a few additional files to operate, one to keep track of the last serial number used by the CA, each certificate must have a unique serial number, and another file to record which certificates have been issued:

```sudo sh -c "echo '01' > /etc/ssl/CA/serial"```  
```sudo touch /etc/ssl/CA/index.txt```  

The third file is a CA configuration file. Though not strictly necessary, it is very convenient when issuing multiple certificates. Edit /etc/ssl/openssl.cnf, and in the [ CA_default ] change:  

`
dir             = /etc/ssl              # Where everything is kept  
database        = $dir/CA/index.txt     # database index file.  
certificate     = $dir/certs/cacert.pem # The CA certificate  
serial          = $dir/CA/serial        # The current serial number  
private_key     = $dir/private/cakey.pem# The private key  
`
Next, create the self-signed root certificate:  

```openssl req -new -x509 -extensions v3_ca -keyout cakey.pem -out cacert.pem -days 3650```  

You will then be asked to enter the details about the certificate.  

Now install the root certificate and key:  

```sudo mv cakey.pem /etc/ssl/private/```  
```sudo mv cacert.pem /etc/ssl/certs/```  

You are now ready to start signing certificates. The first item needed is a Certificate Signing Request (CSR), see Generating a Certificate Signing Request (CSR) for details. Once you have a CSR, enter the following to generate a certificate signed by the CA:  

```sudo openssl ca -in server.csr -config /etc/ssl/openssl.cnf```  

After entering the password for the CA key, you will be prompted to sign the certificate, and again to commit the new certificate. You should then see a somewhat large amount of output related to the certificate creation.  

There should now be a new file, /etc/ssl/newcerts/01.pem, containing the same output. Copy and paste everything beginning with the line: -----BEGIN CERTIFICATE----- and continuing through the line: ----END CERTIFICATE----- lines to a file named after the hostname of the server where the certificate will be installed. For example mail.example.com.crt, is a nice descriptive name.

Subsequent certificates will be named 02.pem, 03.pem, etc.  

Note  

Replace mail.example.com.crt with your own descriptive name.  

Finally, copy the new certificate to the host that needs it, and configure the appropriate applications to use it. The default location to install certificates is /etc/ssl/certs. This enables multiple services to use the same certificate without overly complicated file permissions.  

For applications that can be configured to use a CA certificate, you should also copy the /etc/ssl/certs/cacert.pem file to the /etc/ssl/certs/ directory on each server.  

