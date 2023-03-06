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
    echo "Configuration file not found. Make sure you have configured all values in the specified configuration file."
    exit 1
fi

echo -e "[+] \x1b[1;32mcheck for repos\x1b[0m"
if [ "$Ruuter" == "Y" ]; then
    if [ -d "Ruuter" ]; then
        echo -e "[+] Ruuter clone already exists: checking updates from git"
        cd Ruuter
        git fetch
        git pull
        cd ..
    else
        echo -e "[+] \x1b[1;32mcloning Ruuter\x1b[0m"
        git clone https://github.com/buerokratt/Ruuter.git
    fi
else
    echo "Dont want Ruuter"
fi

if [ "$TIM" == "Y" ]; then
    if [ -d "TIM" ]; then
        echo -e "[+] TIM clone already exists: checking updates from git"
        cd TIM
        git fetch
        git pull
        cd ..
    else
        echo -e "[+] \x1b[1;32mcloning TIM\x1b[0m"
        git clone https://github.com/buerokratt/TIM.git
    fi
else
    echo "Dont want TIM"
fi

if [ "$DataMapper" == "Y" ]; then
    if [ -d "DataMapper" ]; then
        echo -e "[+] DataMapper clone already exists: checking updates from git"
        cd DataMapper
        git fetch
        git pull
        cd ..
    else
        echo -e "[+] \x1b[1;32mcloning DataMapper\x1b[0m"
        git clone https://github.com/buerokratt/DataMapper.git
    fi
else
    echo "Dont want DataMapper"
fi

if [ "$Resql" == "Y" ]; then
    if [ -d "Resql" ]; then
        echo -e "[+] Resql clone already exists: checking updates from git"
        cd Resql
        git fetch
        git pull
        cd ..
    else
        echo -e "[+] \x1b[1;32mcloning Resql\x1b[0m"
        git clone https://github.com/buerokratt/Resql.git
    fi
else
    echo "Dont want Resql"
fi

if [ "$Chat_Widget" == "Y" ]; then
    if [ -d "Chat-Widget" ]; then
        echo -e "[+] Chat-Widget clone already exists: checking updates from git"
        cd Chat-Widget
        git fetch
        git pull
        cd ..
    else
        echo -e "[+] \x1b[1;32mcloning Chat-Widget\x1b[0m"
        git clone https://github.com/buerokratt/Chat-Widget.git
    fi
else
    echo "Dont want Chat-Widget"
fi

if [ "$Buerokratt_Chatbot" == "Y" ]; then
    if [ -d "Buerokratt-Chatbot" ]; then
        echo -e "[+] Buerokratt-Chatbot clone already exists: checking updates from git"
        cd Buerokratt-Chatbot
        git fetch
        git pull
        cd ..
    else
        echo -e "[+] \x1b[1;32mcloning Buerokratt-Chatbot\x1b[0m"
        git clone https://github.com/buerokratt/Buerokratt-Chatbot.git
    fi
else
    echo "Dont want Buerokratt-Chatbot"
fi

if [ "$Training_Module" == "Y" ]; then
    if [ -d "Training-Module" ]; then
        echo -e "[+] Training-Module clone already exists: checking updates from git"
        cd Training-Module
        git fetch
        git pull
        cd ..
    else
        echo -e "[+] \x1b[1;32mcloning Training-Module\x1b[0m"
        git clone https://github.com/buerokratt/Training-Module.git
    fi
else
    echo "Dont want Training-Module"
fi
