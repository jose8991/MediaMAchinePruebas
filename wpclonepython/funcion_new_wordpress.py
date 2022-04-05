import os, sys, stat
from unicodedata import name
from dotenv import load_dotenv
import shutil
import requests
from requests.structures import CaseInsensitiveDict
import mysql.connector

def new_wordpress(NAME,PASSWORD):
    print("entro correctamente ala funcion")
    print(NAME,PASSWORD)
    SOURCE="plugins"
    PORT="80"
    BLOGNAME="TituloGenerico"
    BLOGDESC="descripcionGenerica"
    conexion = mysql.connector.connect(user=os.getenv('WP_DB_USER'), password=os.getenv('WP_DB_PWD'), host=os.getenv('WP_DB_HOST'))
    url = f"https://api.cloudflare.com/client/v4/zones/{os.getenv('ID_DNS')}/dns_records"
    headers = CaseInsensitiveDict()
    headers["X-Auth-Email"] = os.getenv('EMAIL')
    headers["X-Auth-Key"] = os.getenv('KEY')
    headers["Content-Type"] = "application/json"
    data = f"""{{"type":"A","name":"{NAME}","content":"{os.getenv('IP')}","ttl":3600,"priority":10,"proxied":true}}"""

    if (int(os.getenv('ENPRODUCCION')) > 0):
        print("entro al if")
        server=(f"{NAME}.{os.getenv('DOMAIN')}") 
        opval=(f"https://{server}")
        resp = requests.post(url, headers=headers, data=data)
        port=80

    else:
        opval=("http://localhost:"+os.getenv('EMAIL'))
        print(opval)
        server="_"
        port=PORT
    # #creamos el dns
    # #Sacar las URL, EMAIL, KEY, IP para que estén envvars.sh y acá usar las variables

    shutil.copy(f"{os.getenv('MMHOME')}/wpclone/origin", f"/etc/nginx/sites-available/{NAME}")
    print("copio el origin")
    with open(f"/etc/nginx/sites-available/{NAME}", 'r') as file :
      filedata = file.read()
    filedata = filedata.replace('{{port}}', PORT)
    filedata = filedata.replace('{{origin}}', NAME)
    filedata = filedata.replace('{{server_name}}', server)
    # Write the file out again
    with open(f'/etc/nginx/sites-available/{NAME}', 'w') as file:
      file.write(filedata)
    

    os.system(f"ln -s /etc/nginx/sites-available/{NAME} /etc/nginx/sites-enabled/{NAME}")
    os.system("systemctl reload nginx")



    # #creamos la base de datos ,su usuario y le damos sus permisos
    # # Sacar las credenciales y el host (localhost en este caso) para que estén envvars.sh

    curso1=conexion.cursor()
    curso1.execute(f"CREATE DATABASE {NAME}")
    curso1.execute(f"CREATE USER '{NAME}'@'{os.getenv('WP_DB_HOST')}' IDENTIFIED BY '{os.getenv('WP_DB_PWD')}'")
    curso1.execute(f"GRANT ALL PRIVILEGES ON {NAME}.* TO {NAME}@{os.getenv('WP_DB_HOST')}")
    curso1.execute("FLUSH PRIVILEGES")
    
    print("creo la base de datos correctamente")
    if (SOURCE != 'generic'):
      print("entro al if")
      os.system(f"mysqldump  -u{os.getenv('WP_DB_USER')} -p{os.getenv('WP_DB_PWD')} --no-create-db {SOURCE} --single-transaction --compress --order-by-primary | mysql -u{os.getenv('WP_DB_USER')} -p{os.getenv('WP_DB_PWD')} {NAME}")
      print("mysqldump correctamente")
      curso2=conexion.cursor()
      print("creo ok")
      curso2.execute(f"UPDATE {NAME}.wp_options SET option_value='{opval}' WHERE option_name in ('home','siteurl')")
      curso2.execute(f"UPDATE {NAME}.wp_options SET option_value='{BLOGNAME}' WHERE option_name in ('blogname')")
      curso2.execute(f"UPDATE {NAME}.wp_options SET option_value='{BLOGDESC}' WHERE option_name in ('blogdescription')")
      print("aun funcionando")
      
    conexion.close() 
    shutil.copytree(f"{os.getenv('MMHOME')}/wpclone/wordpresscontent/generic/", f"/var/www/{NAME}")
    print("entro al copiado de contemifo")
    shutil.copy(f"{os.getenv('MMHOME')}/wpclone/wordpresscontent/generic/wp-config.php", f"/var/www/{NAME}")



    #permisos
    ruta_a_explorar=f"//var/www/{NAME}/"
    


    with open(f'/var/www/{NAME}/wp-config.php', 'r') as file :
      filedata = file.read()

    # Replace the target stringch
    filedata = filedata.replace('database_name_here', NAME)
    filedata = filedata.replace('username_here', NAME)
    filedata = filedata.replace('password_here', PASSWORD)
    # Write the file out again
    with open(f'/var/www/{NAME}/wp-config.php', 'w') as file:
      file.write(filedata)

