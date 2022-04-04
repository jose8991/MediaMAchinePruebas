import os
from dotenv import load_dotenv
import shutil
import requests
import sys
from requests.structures import CaseInsensitiveDict
import mysql.connector
#ingreso por parametros
variabe = sys.argv[1]
print(variabe)
# # #hutil.copy(f"{os.getenv('MMHOME')}/wpclone/origin", f"/etc/nginx/sites-available/{NAME}")
# a=os.getenv('WP_DB_HOST')
# print(a)
# conexion = mysql.connector.connect(user=os.getenv('WP_DB_USER'), password=os.getenv('WP_DB_PWD'), host=os.getenv('WP_DB_HOST'))
# # curso1=conexion.cursor()
# # curso1.execute(f"CREATE DATABASE {NAME}")
# # curso1.execute(f"CREATE USER '{NAME}'@'{os.getenv('WP_DB_HOST')}' IDENTIFIED BY '{os.getenv('WP_DB_PWD')}'")
# # curso1.execute(f"GRANT ALL PRIVILEGES ON {NAME}.* TO {NAME}@{os.getenv('WP_DB_HOST')}")
# # curso1.execute("FLUSH PRIVILEGES")
# conexion.close()  

# b=os.getenv('ENPRODUCCION')
# print(type(b))
