import mysql.connector
import os
import shutil
SOURCE='generic'
NAME="borrar"

#os.mkdir(f"/var/www/{name}")

os.system(f"cp -r {os.gBuenaetenv('MMHOME')}/wpclone/wordpresscontent/{SOURCE}/* /var/www/{NAME}/")
