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
#replace in files placeholders with $vars
deploy="$buildpath/Installation-Guides/default-setup/chatbot-and-training/bot_training/deploy.sh"
train="$buildpath/Installation-Guides/default-setup/chatbot-and-training/bot_training/train.sh"
echo "$(sed "s|DIR=/your/actual/directory|DIR=$buildpath/Installation-Guides/default-setup/chatbot-and-training/bot/loba|g" $train)" > $train
echo "$(sed "s|DIR=/your/actual/directory|DIR=$buildpath/Installation-Guides/default-setup/chatbot-and-training/bot/loba|g" $deploy)" > $deploy
echo "$(sed "s|BOT_HOST='BOT_HOSTNAME'|BOT_HOST='$keytoolOU'|g" $deploy)" > $deploy
echo "$(sed "s|BOT_USER='BOT_USER'|BOT_USER='$username'|g" $deploy)" > $deploy
echo "$(sed "s|SSH_KEY='SSH_KEY_PATH'|SSH_KEY='$SSH_KEY'|g" $deploy)" > $deploy

cd $buildpath/Installation-Guides/default-setup/chatbot-and-training/bot_training/
mv * $buildpath/../
cd $buildpath
chmod +x deploy.sh train.sh
docker-compose up -d
exec bash
