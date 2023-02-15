#!/bin/bash

#DATA disc mounting
sudo fdisk -l
sudo parted /dev/vdb --script mklabel gpt
sudo mkfs.ext4 -F /dev/vdb
sudo sed -i '2a /dev/vdb    /opt    ext4      defaults        0             0' /etc/fstab
sudo mount -a | grep vdb

#install docker
sudo apt update
sudo apt -y install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
sudo apt -y install docker-ce

#install docker-compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version
sudo usermod -aG docker ${USER}

#move docker to data disk
cd /opt/
cd /var/lib/
sudo mv docker/ /opt/docker
sudo ln -s /opt/docker
ls -al | grep docker
