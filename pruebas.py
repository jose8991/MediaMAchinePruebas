import os
from dotenv import load_dotenv
import shutil
NAME='origin'
#os.system(f"chown -R www-data.www-data /var/www/{NAME}/")
#shutil.copytree(f"{os.getenv('MMHOME')}/wpclone/wordpresscontent/generic/", f"/var/www/{NAME}")

#hutil.copy(f"{os.getenv('MMHOME')}/wpclone/wordpresscontent/generic/wp-config.php", f"/var/www/{NAME}")



#hutil.copy(f"{os.getenv('MMHOME')}/wpclone/origin", f"/etc/nginx/sites-available/{NAME}")
os.system(f"ln -s /etc/nginx/sites-available/{NAME} /etc/nginx/sites-enabled/{NAME}")