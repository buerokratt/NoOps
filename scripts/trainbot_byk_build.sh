#!/bin/bash
#check prerequisites
command -v python3 >/dev/null 2>&1 || { echo >&2 "python is required but it's not installed. "; echo "Installation guide: https://docs.python-guide.org/starting/install3/linux/"; prereq="null"; } && command -v docker >/dev/null 2>&1 || { echo >&2 "docker is required but it's not installed. "; echo "Installation guide: https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04"; prereq="null"; } && command -v docker-compose >/dev/null 2>&1 || { echo >&2 "docker-compose is required but it's not installed. "; echo "Installation guide: https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-20-04"; prereq="null"; }
if [ "$prereq" == "null" ]; then
    echo "Aborting"; exit 1
fi
#show path of config
config="/path/to/config.txt"
#import $vars from config
buildpath=$(sed 's/buildpath=//g;9q;d' $config)
bot_name=$(sed 's/keytoolCN=//g;13q;d' $config)
BOT_HOST=$(sed 's/keytoolOU=//g;14q;d' $config)
BOT_USER=$(sed 's/username=//g;6q;d' $config)
SSH_KEY=$(sed 's/SSH_KEY=//g;23q;d' $config)
BOT_DATA_DIR=$(sed 's/BOT_DATA_DIR=//g;24q;d' $config)
cd $buildpath
git clone https://github.com/buerokratt/Installation-Guides.git
cd Installation-Guides
#replace in files placeholders with $vars
deploy="$buildpath/Installation-Guides/default-setup/chatbot-and-training/bot_training/deploy.sh"
train="$buildpath/Installation-Guides/default-setup/chatbot-and-training/bot_training/train.sh"
echo "$(sed "s|DIR=/your/actual/directory|DIR=$buildpath/Installation-Guides/default-setup/chatbot-and-training/bot/loba|g" $train)" > $train
echo "$(sed "s|DIR=/your/actual/directory|DIR=$buildpath/Installation-Guides/default-setup/chatbot-and-training/bot/loba|g" $deploy)" > $deploy
echo "$(sed "s|BOT_HOST='BOT_HOSTNAME'|BOT_HOST='$BOT_HOST'|g" $deploy)" > $deploy
echo "$(sed "s|BOT_USER='BOT_USER'|BOT_USER='$BOT_USER'|g" $deploy)" > $deploy
echo "$(sed "s|SSH_KEY='SSH_KEY_PATH'|SSH_KEY='$SSH_KEY'|g" $deploy)" > $deploy

cd $buildpath/Installation-Guides/default-setup/chatbot-and-training/bot_training/
mv * $buildpath/../
cd
exec bash
