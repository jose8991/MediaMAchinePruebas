#!/bin/bash
ficheroa=/etc/nginx/sites-available
ficheroe=/etc/nginx/sites-enable
#descargamos los dns en ejecucion y lo guardamos en el archivo dns.json
curl -X GET "https://api.cloudflare.com/client/v4/zones/$ID_DNS/dns_records"      -H "X-Auth-Email: $EMAIL"      -H "X-Auth-Key: $KEY"      -H "Content-Type: application/json" | jq > dns.json
#miramos el numeros de dns activos
jq ".result | length" dns.json
#vamos a recorrer todos los archivos que tenemos en la carpeta sites-available y lo comparamos con la listas y los que esten en la direccion de la carpeta pero no esta en la lista eliminamos el dns y el archivo que esta en la carpeta
for entry in "$ficheroa"/*
do
    #creamos variable booleana la cual la vamos a comparar para la toma de desiciones 
    siEsta=false
    #creamos el ciclo donde me va a recorrer toda la lista
    while IFS=, read col1 col2
        do
        #revisamos si esta el archivo en la carpeta y en la lista y cambiamos el estado del booleano
        if [ $(basename $entry) == $col2 ]
            then
            siEsta=true
            break
        fi
        #termina la iteracion    
        done < $MMHOME/settings/InstaPruebas.csv 
    if $siEsta ; 
    then
        echo "si esta $entry"
    else
        #coguemos solo el nombre del archivo mas no de toda la ruta
        nametodelete=${entry##*/}
        echo "$nametodelete no esta"
        #sacamos el id del dns para guardarlo en la variable para hacer el curl delete para eliminar el dns
        VariableId=$(jq '.result [] | select(.name == "'$nametodelete'.'$DOMAIN'") | .id' dns.json)
        #borramos las comillas para tener el id absoluto
        VariableId=$(echo $VariableId | tr -d '"')
        echo $VariableId
        #eliminamos el dns
        curl -X DELETE "https://api.cloudflare.com/client/v4/zones/$ID_DNS/dns_records/$VariableId"  -H "X-Auth-Email: $EMAIL"  -H "X-Auth-Key: $KEY"  -H "Content-Type: application/json"
        #eliminamos los archivos de la carpetas de nginx
        rm $ficheroa/$nametodelete
        rm $ficheroe/$nametodelete    
    fi
done