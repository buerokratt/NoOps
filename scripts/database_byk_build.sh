#!/bin/bash
echo -e "[+] \x1b[1;32mcheck prerequisites\x1b[0m"
for cmd in docker docker-compose git psql; do
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
sqlcompose="$bykstack_dir/sql-db/docker-compose.yml"
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
sed -i "s|POSTGRES_PASSWORD=123|POSTGRES_PASSWORD=$safe_tim_db|g;
  s|POSTGRES_PASSWORD=01234|POSTGRES_PASSWORD=$safe_byk_db|g;
  s|POSTGRES_PASSWORD=01234|POSTGRES_PASSWORD=$safe_byk_db|g" $sqlcompose
sed -i "s|users-db|$dburl|g" $backofficompose
cd "$bykstack_dir/sql-db/"

#generate_certs
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
give_ownership = """
sudo chown 999:999 cert.crt 
sudo chmod 0600 cert.crt 
 https://stackoverflow.com/questions/55072221/deploying-postgresql-docker-with-ssl-certificate-and-key-with-volumes """
directories = ["users-db", "tim-db"]
 
for directory in directories:
    os.chdir(directory)
    subprocess.check_output(create_cert, shell=True, executable='/bin/bash')
    #give_ownership
    os.chdir("..")
EOF
    )

    python3 -c "$PYCMD"
}
generate-certs

cd tim-db
sudo chown 999:999 key.key
sudo chmod 0600 key.key
sudo chown 999:999 cert.crt
sudo chmod 0600 cert.crt
cd "$bykstack_dir/sql-db/users-db"
sudo chown 999:999 key.key
sudo chmod 0600 key.key
sudo chown 999:999 cert.crt
sudo chmod 0600 cert.crt
cd $bykstack_dir/sql-db/
docker-compose up -d
if [ $( docker ps -a -f name=users-db | wc -l ) -eq 2 ]; then
  status=$( docker ps -a -f name=users-db | grep users-db 2> /dev/null )
  output=$( echo ${status} | awk '{ print $7}' )
  echo "$output"
  if [ $output == "Up" ]; then
    docker run --network=bykstack riaee/byk-users-db:liquibase20220615 bash -c "sleep 5 && liquibase --url=jdbc:postgresql://$dburl:5433/byk?user=byk --password=$safe_byk_db --changelog-file=/master.yml update"
    psqlcommand="insert into configuration(key, value) values ('bot_institution_id', '$bot_name');"
    psqlcommand2='"'$psqlcommand'"'
    docker run --network=bykstack ubuntu:latest bash -c "apt-get -y update && apt-get -y install postgresql-client && PGPASSWORD=$safe_byk_db psql -d byk -U byk -h users-db -p 5432 -c $psqlcommand2 -c 'CREATE EXTENSION hstore;'"
  else
   echo "users-db exists, but is not Up"
  fi

else
  echo "users-db does not exist"
  exit 1 
fi
if [ $( docker ps -a -f name=tim-postgresql | wc -l ) -eq 2 ]; then
  status=$( docker ps -a -f name=tim-postgresql | grep tim-postgresql 2> /dev/null )
  output=$( echo ${status} | awk '{ print $7}' )
  echo "$output"
  if [ $output == "Up" ]; then
    docker exec tim-postgresql bash -c "createdb -O tim -e -U tim tim"
  else
   echo "tim-postgresql exists, but is not Up"
  fi
  
else
  echo "tim-postgresql does not exist"
  exit 1 
fi
cd "$buildpath"
