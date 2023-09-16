#!bin/bash
sudo su
apt-get update

apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo \
  "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

apt-get update

 apt-get install -y docker-ce docker-ce-cli containerd.io

 usermod -aG docker $USER

 apt install docker-compose -y

docker --version

apt install python3-pip -y

pip3 install telebot 

git clone https://github.com/AndrewKrmn/AWS_X_Python-bot-.git

cd AWS_X_Python-bot-/ && python3 telegram.py






