#!/bin/bash
echo -e "[+] \x1b[1;32mcheck prerequisites\x1b[0m"
for cmd in docker docker-compose git; do
    if ( ! which "$cmd" > /dev/null 2>&1 ); then
        echo -e "[+] \x1b[1;33mCommand '$cmd' is required, but not installed! Aborting.\x1b[0m"
        exit 1
    else
        echo -e "[+] Command '$cmd' is installed"
    fi
done

echo -e "[+] \x1b[1;32mimport variables from config\x1b[0m"
if [ -f "config.sh" ]; then
    source config.sh
else
    echo -e "[+] \x1b[1;33mConfiguration file not found. Make sure you have configured all values in the specified configuration file.\x1b[0m"
    exit 1
fi

bykstack_dir="$buildpath/Installation-Guides/default-setup/backoffice-and-bykstack"
publicurls="$bykstack_dir/ruuter/public.urls.docker.json"
privateurls="$bykstack_dir/ruuter/private.urls.docker.json"
index="$bykstack_dir/chat-widget/index.html"
chatnginx="$bykstack_dir/chat-widget/nginx.conf"
envconfig="$bykstack_dir/customer-support/env-config.js"
customernginx="$bykstack_dir/customer-support/nginx.conf"
timdockercompose="$bykstack_dir/tim/docker-compose.yml"
backofficompose="$bykstack_dir/docker-compose.yml"

echo -e "[+] \x1b[1;32mcheck for repos\x1b[0m"
if [ -d "Installation-Guides" ]; then
    echo -e "[+] repo already exists: checking updates from git"
    cd Installation-Guides
    git fetch
    git pull
    cd ..
else
    echo -e "[+] cloning repo from git"
    git clone https://github.com/buerokratt/Installation-Guides.git
fi

echo -e "[+] \x1b[1;32mreplace in files placeholders with config values\x1b[0m"
sed -i "s|http://BOT_IP:5005|http://$bot_url|g;
    s|TRAINIG_BOT_PRIVATE_SSH_KEY_PATH|$training_prv_key|g;
    s|TRAINIG_BOT|$training_url|g;
    s|TRAINING_BOT_USERNAME|$training_user|g;
    s|TRAINING_DATA_DIRECTORY|$training_bot_dir|g" $publicurls
sed -i "s|http://BOT_IP:5005|http://$bot_url|g;
    s|TRAINIG_BOT_PRIVATE_SSH_KEY_PATH|$training_prv_key|g;
    s|TRAINIG_BOT|$training_url|g;
    s|TRAINING_BOT_USERNAME|$training_user|g;
    s|TRAINING_DATA_DIRECTORY|$training_bot_dir|g" $privateurls
sed -i "s|https://ruuter.test.buerokratt.ee|$public_ruuter|g;
    s|https://TIM_URL|$tim|g;
    s|https://URL_WHERE_TO_WIDGET_IS_INSTALLED|$widget|g" $index
sed -i "s|https://URL_WHERE_TO_WIDGET_IS_INSTALLED|$widget|g" $chatnginx
sed -i "s|https://PRIVATE_RUUTER_URL|$private_ruuter|g;
    s|https://TIM_URL|$tim|g;
    s|https://CUSTOMER_SERVICE_URL|$back_office|g" $envconfig
sed -i "s|https://RUUTER_URL|$public_ruuter|g;
    s|https://TIM_URL|$tim|g;
    s|https://CUSTOMER_SERVICE_URL|$back_office|g;
    s|https://PRIV-RUUTER_URL|$private_ruuter|g" $customernginx
sed -i "s|spring.datasource.password=123|spring.datasource.password=$safe_tim_db|g;
    s|POSTGRES_PASSWORD=123|POSTGRES_PASSWORD=$safe_byk_db|g" $timdockercompose
sed -i "s|spring.datasource.password=123|spring.datasource.password=$safe_tim_db|g;
    s|https://buerokratt.ee|$back_office|g;
    s|https://admin.buerokratt.ee|$widget|g;
    s|https://tim.buerokratt.ee|$tim|g;
    s|tim-postgresql:5432|$timdb|g;
    s|tara_client_id|$taraid|g;
    s|tara_client_secret|$tarapass|g;
    s|https://tim.byk.buerokratt.ee|$tim|g;
    s|https://admin.byk.buerokratt.ee|$back_office|g;
    s|https://byk.buerokratt.ee|$widget|g;
    s|https://ruuter.byk.buerokratt.ee|$public_ruuter|g;
    s|https://priv-ruuter.byk.buerokratt.ee|$private_ruuter|g;
    s|https://priv-ruuter.buerokratt.ee|$private_ruuter|g;
    s|jwt-integration.signature.issuer=byk.buerokratt.ee|jwt-integration.signature.issuer=$keytoolCN.$keytoolOU.$keytoolC|g;
    s|safe_keystore_password|$keytoolpass|g;
    s|password=01234|password=$safe_byk_db|g" $backofficompose

echo -e "[+] \x1b[1;32mtim keys\x1b[0m"
cd "$bykstack_dir/tim"
if [ -f jwtkeystore.jks ] && [ "$(cat "jwtkeystore.jks")" ]; then
    echo "[+] jwtkeystore.jks: file exists, skipping creating it in tim-byk-tim-1"
else
    keytools="'CN=$keytoolCN, OU=$keytoolOU, O=PLACEHOLDER, L=PLACEHOLDER, S=PLACEHOLDER, C=$keytoolC'"
    docker-compose up -d && \
        docker exec tim_byk-tim_1 bash -c "keytool -genkeypair -alias jwtsign -keyalg RSA -keysize 2048 -keystore 'jwtkeystore.jks' -validity 3650 -noprompt -dname $keytools -storepass $keytoolpass" && \
        docker cp tim_byk-tim_1:/usr/local/tomcat/jwtkeystore.jks jwtkeystore.jks && \
        sudo chown $username jwtkeystore.jks
        docker-compose down
fi

#generate_certs
echo -e "[+] \x1b[1;32mgenerate certs\x1b[0m"
cd "$bykstack_dir"
# for dir in customer-support ruuter dmapper chat-widget tim resql; do
#     cert="$bykstack_dir/$dir/cert.crt"
#     key="$bykstack_dir/$dir/key.key"
#     if [ -r "$cert" ] && [ "$(cat "$cert")" ]; then
#         echo "$cert: certificate file exists, skipping"
#         continue
#     fi
#     eval cert_config="\$$(echo "$dir" | sed 's/-/_/g')_cert"
#     eval key_config="\$$(echo "$dir" | sed 's/-/_/g')_key"
#     if [ "$cert_config" ]; then
#         if [ ! -f "$cert_config" ]; then
#             echo "$cert_config: file does not exist, but is configured to be used for '$cert'! Aborting."
#             exit 1
#         fi
#         cp -pv "$cert_config" "$cert"
#         cp -pv "$key_config" "$key"
#     else
#         openssl req -out "$cert" -keyout "$key" -newkey rsa:4096 -x509 -sha256 -days 3980 -nodes -subj "$default_cert_subj"
#     fi
# done

generate-certs (){
    PYCMD=$(cat <<EOF
import os
import subprocess

create_cert = """openssl req -newkey rsa:4096 \
            -x509 \
            -sha256 \
            -days 3980 \
            -nodes \
            -out cert.crt \
            -keyout key.key \
            -subj "/C=oo/ST=Create/L=your/O=certs/OU=lazy IT Department/CN=default.value"   """

give_ownership = """ https://stackoverflow.com/questions/55072221/deploying-postgresql-docker-with-ssl-certificate-and-key-with-volumes """

directories = ["customer-support", "ruuter", "dmapper", "chat-widget", "tim", "resql"]
 
for directory in directories:
    os.chdir(directory)
    subprocess.check_output(create_cert, shell=True, executable='/bin/bash')
    os.chdir("..")

EOF
    )

    python3 -c "$PYCMD"
}
generate-certs
#bykstack
docker-compose up -d
cd "$buildpath"

