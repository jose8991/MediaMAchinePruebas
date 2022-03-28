from distutils.command.config import dump_file
from re import I
import pandas as pd
import os
import requests
import json
from requests.structures import CaseInsensitiveDict
from dotenv import load_dotenv
#add dns subdomain names to a list
def lista_dns(IDNS=os.getenv('ID_DNS'),EMAIL=os.getenv('EMAIL'),KEY=os.getenv('KEY')):
    list=[]
    url = f"https://api.cloudflare.com/client/v4/zones/{IDNS}/dns_records"
    headers = CaseInsensitiveDict()
    headers["X-Auth-Email"] = EMAIL
    headers["X-Auth-Key"] = KEY
    headers["Content-Type"] = "application/json"
    resp = requests.get(url, headers=headers)
    respuesta=json.loads(resp.text)
    for r in respuesta["result"]:
        a=(r["name"][:r["name"].index(".")])
        list.append(a)
    return list
ListaDns=lista_dns()
LocationFile=f"{os.getenv('MMHOME')}/settings/InstaPruebas.csv"
df=pd.read_csv(LocationFile, header=None)

ElementListCsv=df[1].values

for i in ElementListCsv:
    iteracion=os.path.exists(f'/etc/nginx/sites-available/{i}')
    EstaEnDns=i in ListaDns
    if (iteracion or EstaEnDns):
        print(i) 
    else:
        print(f"no esta {i}")
    

