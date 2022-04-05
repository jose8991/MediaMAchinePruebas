#!/bin/bash
#instalamos lemp
apt-get install nginx -y
sudo apt install vim -y
apt remove netfilter-persistent
apt update
apt upgrade -y
apt remove netfilter-persistent 
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 3306/tcp
ufw allow 5000/tcp
pip install pandas
echo "y" | ufw enable
apt-get install php-fpm -y
apt-get install mysql-server php-mysql -y
sudo apt install php-fpm php-common php-mbstring php-xmlrpc php-soap php-gd php-xml php-intl php-mysql php-cli php-ldap php-zip php-curl -y
sudo apt-get install jq
python -m pip install python-dotenv
python -m pip install requests
pip install mysql-connector
pip install mysql-connector-python

echo "yes" | git clone --branch testfunction git@github.com:jfernandrezj/media_machine.git
##1
sudo mysql -u$WP_DB_USER -p$WP_DB_PWD -e "create database plugins;"
sudo mysql -u$WP_DB_USER -p$WP_DB_PWD plugins < $MMHOME/wpclone/plugins.backup.sql