#!/bin/bash

mkdir certs
cd certs

# For local purposes, we'll create our own self-signed CA.

# Create the configuration file
touch csr.cnf
echo "[req]
default_bits = 4096
distinguished_name = dn
prompt             = no
req_extensions = req_ext

[dn]
C="EE"
ST="Estonia"
L="Talinn"
O="Burokratt"
OU="Tech"
emailAddress="developer@burokratt.com"
CN="ca"

[req_ext]
subjectAltName = @alt_names
basicConstraints = critical, CA:true, pathlen:0

[alt_names]
DNS.0 = *localhost" > csr.cnf


# Create a private key for the self-signed CA
openssl genrsa -out ca-key.pem 4096

# Create a self-signed certificate for the self-signed  CA
openssl req -x509 -new -nodes -key ca-key.pem -sha256 -days 365 -out ca.pem --extensions req_ext -config csr.cnf

# Verify the certificate
openssl verify -CAfile ca.pem ca.pem

# Define the pods that will be signed using the same CA
pods=("ruuter" "resql" "tim" "data-mapper" "analytics" "service" "training" "chatbot" "widget")

for element in "${pods[@]}"; do
    
    # Create a directory for the pod
    mkdir ${element}

    # Navigate to the pod directory
    cd ${element}

    # Create the configuration file
    touch ${element}-csr.cnf
    echo "[req]
    default_bits = 4096
    distinguished_name = dn
    prompt             = no
    req_extensions = req_ext

    [dn]
    C="EE"
    ST="Estonia"
    L="Talinn"
    O="Burokratt"
    OU="Tech"
    emailAddress="developer@burokratt.com"
    CN="${element}"

    [req_ext]
    subjectAltName = @alt_names

    [alt_names]
    DNS.0 = *localhost" > ${element}-csr.cnf

    # Create a private key for the pod
    openssl genrsa -out ${element}-key.pem 4096
    
    # Create a CSR (Certificate Signing Requests) for the pod
    openssl req -new -key ${element}-key.pem -out ${element}-csr.pem -config ${element}-csr.cnf
    
    # Sign the CSR (Certificate Signing Requests) with the CA to generate the server certificate
    openssl x509 -req -days 365 -in ${element}-csr.pem -CA ../ca.pem -CAkey ../ca-key.pem -CAcreateserial -out ${element}-cert.pem --extensions req_ext -extfile ${element}-csr.cnf

    # Verify the certificate
    openssl verify -CAfile ../ca.pem ${element}-cert.pem

    # Create a PKCS12 file for the pod
    openssl pkcs12 -export -in ${element}-cert.pem -inkey ${element}-key.pem -out ${element}.p12 -passin pass:t9n5Kmm7vP945678 -password pass:t9n5Kmm7vP945678

    # Create a KeyStore file for the pod
    keytool -import -noprompt -trustcacerts -alias ${element}-trust -file ${element}-cert.pem -keystore ${element}-truststore.jks --srcstorepass t9n5Kmm7vP945678 -deststorepass t9n5Kmm7vP945678

    # Navigate back to the certs directory
    cd ..
done
