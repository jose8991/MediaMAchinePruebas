import os, sys, stat
from unicodedata import name
from dotenv import load_dotenv
import shutil
import requests
from requests.structures import CaseInsensitiveDict
import mysql.connector

NAME="borrarfinaltest11"
PASSWORD="Jose123-"
SOURCE="generic"
PORT="80"
BLOGNAME="TituloGenerico"
BLOGDESC="descripcionGenerica"
#conexion = mysql.connector.connect(user=os.getenv('WP_DB_USER'), password=os.getenv('WP_DB_PWD'), host=os.getenv('WP_DB_HOST'))
url = f"https://api.cloudflare.com/client/v4/zones/{os.getenv('ID_DNS')}/dns_records"
headers = CaseInsensitiveDict()
headers["X-Auth-Email"] = os.getenv('EMAIL')
headers["X-Auth-Key"] = os.getenv('KEY')
headers["Content-Type"] = "application/json"
data = f"""{{"type":"A","name":"{NAME}","content":"{os.getenv('IP')}","ttl":3600,"priority":10,"proxied":true}}"""

if (int(os.getenv('ENPRODUCCION')) > 0):
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

# curso1=conexion.cursor()
# curso1.execute(f"CREATE DATABASE {NAME}")
# curso1.execute(f"CREATE USER '{NAME}'@'{os.getenv('WP_DB_HOST')}' IDENTIFIED BY '{os.getenv('WP_DB_PWD')}'")
# curso1.execute(f"GRANT ALL PRIVILEGES ON {NAME}.* TO {NAME}@{os.getenv('WP_DB_HOST')}")
# curso1.execute("FLUSH PRIVILEGES")
# conexion.close()  

if (SOURCE != 'generic'):
  pass
  #os.system(f"mysqldump  -u{os.getenv('WP_DB_USER')} -p{os.getenv('WP_DB_PWD')} --no-create-db {SOURCE} --single-transaction --compress --order-by-primary | mysql -u{os.getenv('WP_DB_USER')} -p{os.getenv('WP_DB_PWD')} {NAME}")
  # curso2=conexion.cursor()
  # curso2.execute(f"UPDATE {NAME}.wp_options SET option_value='{opval}' WHERE option_name in ('home','siteurl')")
  # curso2.execute(f"UPDATE {NAME}.wp_options SET option_value='{BLOGNAME}' WHERE option_name in ('blogname')")
  # curso2.execute(f"UPDATE {NAME}.wp_options SET option_value='{BLOGDESC}' WHERE option_name in ('blogdescription')")


shutil.copytree(f"{os.getenv('MMHOME')}/wpclone/wordpresscontent/generic/", f"/var/www/{NAME}")
shutil.copy(f"{os.getenv('MMHOME')}/wpclone/wordpresscontent/generic/wp-config.php", f"/var/www/{NAME}")


os.system(f"chown -R www-data.www-data /var/www/{NAME}/")
#permisos
ruta_a_explorar=f"//var/www/{NAME}/"
 
for root,dirs,files in os.walk(ruta_a_explorar):
        for file in [f for f in files]:
                pp=os.path.join(root, file).replace("""\\""",'/')
                if stat.S_ISDIR(os.stat(pp)[stat.ST_MODE]):
                        os.chmod(pp,stat.S_IRWXU|stat.S_IWUSR|stat.S_IRGRP|stat.S_IXGRP|stat.S_IROTH|stat.S_IXOTH)
                elif stat.S_ISREG(os.stat(pp)[stat.ST_MODE]):
                        os.chmod(pp,stat.S_IRUSR|stat.S_IWUSR|stat.S_IRGRP|stat.S_IROTH)
 
        for dir in [f for f in dirs]:
                pp=os.path.join(root, dir).replace("""\\""",'/')
                print (pp)
                if stat.S_ISDIR(os.stat(pp)[stat.ST_MODE]):
                        os.chmod(pp,stat.S_IRWXU|stat.S_IWUSR|stat.S_IRGRP|stat.S_IXGRP|stat.S_IROTH|stat.S_IXOTH)
                elif stat.S_ISREG(os.stat(pp)[stat.ST_MODE]):
                        os.chmod(pp,stat.S_IRUSR|stat.S_IWUSR|stat.S_IRGRP|stat.S_IROTH)

with open(f'/var/www/{NAME}/wp-config.php', 'r') as file :
  filedata = file.read()

# Replace the target stringch
filedata = filedata.replace('database_name_here', NAME)
filedata = filedata.replace('username_here', NAME)
filedata = filedata.replace('password_here', PASSWORD)
# Write the file out again
with open(f'/var/www/{NAME}/wp-config.php', 'w') as file:
  file.write(filedata)

