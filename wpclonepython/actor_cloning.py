from distutils.command.config import dump_file
import pandas as pd
import os ,json, requests
from requests.structures import CaseInsensitiveDict
from dotenv import load_dotenv
import funcion_new_wordpress

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
#we add the elements of the csv in the list
LocationFile=f"{os.getenv('MMHOME')}/settings/insta_wp_map.csv"
df=pd.read_csv(LocationFile, header=None)
ElementListCsv=df[1].values

#we iterate all the elements of the csv list and those that do not exist we call the new_wordpresss function to create the wordpress
for i in ElementListCsv:
    print("entro correctamente al ciclo for")
    iteracion=os.path.exists(f'/etc/nginx/sites-available/{i}')
    EstaEnDns=i in ListaDns
    if (iteracion or EstaEnDns):
        print(i) 
    else:
        funcion_new_wordpress.new_wordpress(i,os.getenv("WP_DB_PWD"))  
    

