from distutils.command.config import dump_file
import pandas as pd
import os ,json, requests
from requests.structures import CaseInsensitiveDict
from dotenv import load_dotenv
#add dns subdomain names to a list
"https://api.cloudflare.com/client/v4/zones/$ID_DNS/dns_records/$VariableId"

list=[]
listid=[]
url = f"https://api.cloudflare.com/client/v4/zones/{os.getenv('ID_DNS')}/dns_records"
headers = CaseInsensitiveDict()
headers["X-Auth-Email"] = os.getenv('EMAIL')
headers["X-Auth-Key"] = os.getenv('KEY')
headers["Content-Type"] = "application/json"
resp = requests.get(url, headers=headers)
respuesta=json.loads(resp.text)


url_delete=f"https://api.cloudflare.com/client/v4/zones/{os.getenv('ID_DNS')}/dns_records/borrarrrrrrrrrr"
resp2 = requests.delete(url_delete, headers=headers)
for r in respuesta["result"]:
    a=(r["name"][:r["name"].index(".")])
    list.append(a)




LocationFile=f"{os.getenv('MMHOME')}/settings/InstaPruebas.csv"
df=pd.read_csv(LocationFile, header=None)

ElementListCsv=df[1].values

for i in list:
    iteracion=os.path.exists(f'/etc/nginx/sites-available/{i}')
    if i in ElementListCsv or iteracion:
        print(f"esta {i}")
    else:
        # url_delete=f"https://api.cloudflare.com/client/v4/zones/{os.getenv('ID_DNS')}/dns_records/{i}"
        # resp2 = requests.delete(url_delete, headers=headers)
        print(f"no esta {i}")
           
    
     