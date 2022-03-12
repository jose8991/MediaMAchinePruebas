
#!/bin/bash
if [[ $# -eq 0 ]] ; then
    echo 'Need the name and password'
    exit 0
fi
#parametros para la creacion del wordpress
NAME="$1"
PASSWORD="$2"
SOURCE="${3:-generic}"
PORT="${4:-80}"
BLOGNAME="${6:-TituloGenerico}"
BLOGDESC="${7:-descripcionGenerica}"


if [ $ENPRODUCCION -gt 0 ]
then
    server=$NAME.$DOMAIN   
    opval=https://$server
    curl -X POST "https://api.cloudflare.com/client/v4/zones/$ID_DNS/dns_records" \
     -H "X-Auth-Email: $EMAIL" \
     -H "X-Auth-Key: $KEY" \
     -H "Content-Type: application/json" \
     --data '{"type":"A","name":"'$NAME'","content":"'$IP'","ttl":3600,"priority":10,"proxied":true}'
    port=80

else
    opval=http://localhost:$PORT
    server="_"
    port=$PORT
fi
#creamos el dns
#Sacar las URL, EMAIL, KEY, IP para que estén envvars.sh y acá usar las variables
cp $MMHOME/wpclone/origin /etc/nginx/sites-available/${NAME}
sed -i "s/{{port}}/$PORT/g" /etc/nginx/sites-available/${NAME}
sed -i "s/{{origin}}/$NAME/g" /etc/nginx/sites-available/${NAME}
sed -i "s/{{server_name}}/$server/g" /etc/nginx/sites-available/${NAME}
ln -s /etc/nginx/sites-available/${NAME} /etc/nginx/sites-enabled/${NAME}
systemctl reload nginx


#creamos la base de datos ,su usuario y le damos sus permisos
# Sacar las credenciales y el host (localhost en este caso) para que estén envvars.sh


mysql -u$WP_DB_USER -p$WP_DB_PWD -e "CREATE DATABASE $NAME;"
mysql -u$WP_DB_USER -p$WP_DB_PWD -e "CREATE USER '$NAME'@$WP_DB_HOST IDENTIFIED BY '$PASSWORD';"
mysql -u$WP_DB_USER -p$WP_DB_PWD -e "GRANT ALL PRIVILEGES ON $NAME.* TO $NAME@$WP_DB_HOST;"
mysql -u$WP_DB_USER -p$WP_DB_PWD -e "FLUSH PRIVILEGES;"


if [ $SOURCE != 'generic' ]
then
mysqldump  -u$WP_DB_USER -p$WP_DB_PWD --no-create-db $SOURCE --single-transaction --compress --order-by-primary | mysql -u$WP_DB_USER -p$WP_DB_PWD $NAME
mysql -u$WP_DB_USER -p$WP_DB_PWD -e "UPDATE $NAME.wp_options SET option_value='$opval' WHERE option_name in ('home','siteurl');"
mysql -u$WP_DB_USER -p$WP_DB_PWD -e "UPDATE $NAME.wp_options SET option_value='$BLOGNAME' WHERE option_name in ('blogname');"
mysql -u$WP_DB_USER -p$WP_DB_PWD -e "UPDATE $NAME.wp_options SET option_value='$BLOGDESC' WHERE option_name in ('blogdescription');"
fi



mkdir /var/www/${NAME}
cp -r $MMHOME/wpclone/wordpresscontent/${SOURCE}/* /var/www/${NAME}/
cp -r $MMHOME/wpclone/wordpresscontent/generic/wp-config.php /var/www/${NAME}/
sudo find /var/www/${NAME} -type d -exec chmod 0755 {} \;
sudo find /var/www/${NAME} -type f -exec chmod 0644 {} \;
chown -R www-data.www-data /var/www/${NAME}/

sed -i "s/database_name_here/$NAME/g" /var/www/${NAME}/wp-config.php
sed -i "s/username_here/$NAME/g" /var/www/${NAME}/wp-config.php
sed -i "s/password_here/$PASSWORD/g" /var/www/${NAME}/wp-config.php



