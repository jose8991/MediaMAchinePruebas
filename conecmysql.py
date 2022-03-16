import mysql.connector
import os
from dotenv import load_dotenv
conexion = mysql.connector.connect(user=os.getenv('WP_DB_USER'), password=os.getenv('WP_DB_PWD'), host='localhost')
curso1=conexion.cursor()
curso1.execute("create database borrar19mar")
curso1.execute("show databases")
for base in curso1:
    print(base)
conexion.close()