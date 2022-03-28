import os
from dotenv import load_dotenv
import shutil
import requests
from requests.structures import CaseInsensitiveDict
import mysql.connector
NAME='borrarrrrrrrrrr'
# #os.system(f"chown -R www-data.www-data /var/www/{NAME}/")
# #shutil.copytree(f"{os.getenv('MMHOME')}/wpclone/wordpresscontent/generic/", f"/var/www/{NAME}")
# url = f"https://api.cloudflare.com/client/v4/zones/{os.getenv('ID_DNS')}/dns_records"
# headers = CaseInsensitiveDict()
# headers["X-Auth-Email"] = os.getenv('EMAIL')
# headers["X-Auth-Key"] = os.getenv('KEY')
# headers["Content-Type"] = "application/json"
# data = f"""{{"type":"A","name":"{NAME}","content":"54.208.136.12","ttl":3600,"priority":10,"proxied":true}}"""
# resp = requests.post(url, headers=headers, data=data)
# #hutil.copy(f"{os.getenv('MMHOME')}/wpclone/wordpresscontent/generic/wp-config.php", f"/var/www/{NAME}")
# a='{"type":"A","name":"pruebadesdepyth3on","content":"54.208.136.12","ttl":3600,"priority":10,"proxied":true}'
# print(a)
# b=f"""'{{"type":"A","name":"{NAME}","content":"54.208.136.12","ttl":3600,"priority":10,"proxied":true}}'"""
# print(b)

# #hutil.copy(f"{os.getenv('MMHOME')}/wpclone/origin", f"/etc/nginx/sites-available/{NAME}")
a=os.getenv('WP_DB_HOST')
print(a)
conexion = mysql.connector.connect(user=os.getenv('WP_DB_USER'), password=os.getenv('WP_DB_PWD'), host=os.getenv('WP_DB_HOST'))
# curso1=conexion.cursor()
# curso1.execute(f"CREATE DATABASE {NAME}")
# curso1.execute(f"CREATE USER '{NAME}'@'{os.getenv('WP_DB_HOST')}' IDENTIFIED BY '{os.getenv('WP_DB_PWD')}'")
# curso1.execute(f"GRANT ALL PRIVILEGES ON {NAME}.* TO {NAME}@{os.getenv('WP_DB_HOST')}")
# curso1.execute("FLUSH PRIVILEGES")
conexion.close()  

b=os.getenv('ENPRODUCCION')
print(type(b))
