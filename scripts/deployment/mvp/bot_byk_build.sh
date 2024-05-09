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
cd $buildpath
git clone https://github.com/buerokratt/Installation-Guides.git
cd Installation-Guides
cd $buildpath/Installation-Guides/default-setup/chatbot-and-training/bot/
docker-compose up -d

cd
exec bash
