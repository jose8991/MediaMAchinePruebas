
import mysql.connector
import os
#from dotenv import load_dotenv
NAME='MARBORRARr522'
conexion = mysql.connector.connect(user=os.getenv('WP_DB_USER'), password=os.getenv('WP_DB_PWD'), host=os.getenv('WP_DB_HOST'))
curso1=conexion.cursor()
curso1.execute(f"CREATE DATABASE {NAME}")
curso1.execute(f"CREATE USER '{NAME}'@'{os.getenv('WP_DB_HOST')}' IDENTIFIED BY '{os.getenv('WP_DB_PWD')}'")
curso1.execute(f"GRANT ALL PRIVILEGES ON {NAME}.* TO {NAME}@{os.getenv('WP_DB_HOST')}")
curso1.execute("FLUSH PRIVILEGES")
conexion.close()
#curso1.execute(f"CREATE USER borrar24mar@{os.getenv('WP_DB_HOST')} IDENTIFIED BY {os.getenv('WP_DB_PWD')}")
#curso1.execute(f"CREATE USER {NAME}@{os.getenv('WP_DB_HOST')} IDENTIFIED BY {os.getenv('WP_DB_PWD')}")
#a= f"GRANT ALL PRIVILEGES ON {NAME}.* TO {NAME}@{os.getenv('WP_DB_HOST')}"
#print(a)

# mysql -u$WP_DB_USER -p$WP_DB_PWD -e "CREATE DATABASE $NAME;"
# mysql -u$WP_DB_USER -p$WP_DB_PWD -e "CREATE USER '$NAME'@$WP_DB_HOST IDENTIFIED BY '$PASSWORD';"
# mysql -u$WP_DB_USER -p$WP_DB_PWD -e "GRANT ALL PRIVILEGES ON $NAME.* TO $NAME@$WP_DB_HOST;"
# mysql -u$WP_DB_USER -p$WP_DB_PWD -e "FLUSH PRIVILEGES;"