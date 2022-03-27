import os
from dotenv import load_dotenv
import shutil
import requests
from requests.structures import CaseInsensitiveDict
NAME='borrarrrrrrrrrr'
#os.system(f"chown -R www-data.www-data /var/www/{NAME}/")
#shutil.copytree(f"{os.getenv('MMHOME')}/wpclone/wordpresscontent/generic/", f"/var/www/{NAME}")
url = f"https://api.cloudflare.com/client/v4/zones/{os.getenv('ID_DNS')}/dns_records"
headers = CaseInsensitiveDict()
headers["X-Auth-Email"] = os.getenv('EMAIL')
headers["X-Auth-Key"] = os.getenv('KEY')
headers["Content-Type"] = "application/json"
data = f"""{{"type":"A","name":"{NAME}","content":"54.208.136.12","ttl":3600,"priority":10,"proxied":true}}"""
resp = requests.post(url, headers=headers, data=data)
#hutil.copy(f"{os.getenv('MMHOME')}/wpclone/wordpresscontent/generic/wp-config.php", f"/var/www/{NAME}")
a='{"type":"A","name":"pruebadesdepyth3on","content":"54.208.136.12","ttl":3600,"priority":10,"proxied":true}'
print(a)
b=f"""'{{"type":"A","name":"{NAME}","content":"54.208.136.12","ttl":3600,"priority":10,"proxied":true}}'"""
print(b)

#hutil.copy(f"{os.getenv('MMHOME')}/wpclone/origin", f"/etc/nginx/sites-available/{NAME}")
