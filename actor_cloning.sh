#!/bin/bash

#en fichero se guardara la ruta donde revisaremos si existe el archivo de nginx
fichero=/etc/nginx/sites-available

#vamos a tener la misma contrase;a por defecto y siempre
#me va a crear los sitios con los plugins ya establecidos
PASSWORD="${1:-Borrar123-}"
SOURCE="${2:-plugins}"

#Código que itera la lista de insta_wp_map.csv y revisa que sitios hay que crear y qué sitios hay que eliminar
while IFS=, read col1 col2

do
  
  if [ -f $fichero/$col2 ]
  then 
    #echo "esta"
    echo $col2
    echo "/'$fichero"
else
  ./new_wordpress_from_source.sh $col2 $PASSWORD $SOURCE
  echo $col2 
fi
 
done < $MMHOME/settings/InstaPruebas.csv 


