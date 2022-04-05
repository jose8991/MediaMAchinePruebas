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
print("guardo dns correctamente en la lista")
#agregamos los elemetos del csv en la lista
LocationFile=f"{os.getenv('MMHOME')}/settings/InstaPruebasActor.csv"
df=pd.read_csv(LocationFile, header=None)
ElementListCsv=df[1].values
print("leyo correctamente el archivo csv")

#iteramos todos los elementos de la lista csv y los que no existen llamamos la funcion new_wordpresss para crear el wordpress
for i in ElementListCsv:
    print("entro correctamente al ciclo for")
    iteracion=os.path.exists(f'/etc/nginx/sites-available/{i}')
    EstaEnDns=i in ListaDns
    if (iteracion or EstaEnDns):
        print(i) 
    else:
        funcion_new_wordpress.new_wordpress(i,os.getenv("WP_DB_PWD"))  
    

