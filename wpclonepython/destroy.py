from distutils.command.config import dump_file
import pandas as pd
import os ,json, requests
from requests.structures import CaseInsensitiveDict
from dotenv import load_dotenv

#llamamos a la api de cloudflare con sus credenciales
url = f"https://api.cloudflare.com/client/v4/zones/{os.getenv('ID_DNS')}/dns_records"
headers = CaseInsensitiveDict()
headers["X-Auth-Email"] = os.getenv('EMAIL')
headers["X-Auth-Key"] = os.getenv('KEY')
headers["Content-Type"] = "application/json"

#extraemos el json de los dns exisentes de cloudflare
resp = requests.get(url, headers=headers)
respuesta=json.loads(resp.text)
dns_dict={}
#guardamos en un diccionario como clave el nombre del subdominio y como valor el id que lo representa
for r in respuesta["result"]:
    a=r["name"].split(".",1)[0]
    dns_dict[a]=r["id"]

    
#leemos el csv que queremos revisar y lo metemos en una lista que contenga los valores de la segunda fila
locationFile=f"{os.getenv('MMHOME')}/settings/InstaPruebas.csv"
df=pd.read_csv(locationFile, header=None)
elementListCsv=df[1].values

#recorremos el diccionario y lo comporamos si existe en la lista elementListCsv y si existe en la ruta de nginx
#si no exite en ninguna de las dos lo borra
for i in dns_dict:
    iteracion=os.path.exists(f'/etc/nginx/sites-available/{i}')
    if i in elementListCsv or iteracion:
        print(f"esta {i}")
    else:
        print(f"no esta {i}")
       
        to_delete=dns_dict[i]
        print(to_delete)
        url_delete=f"https://api.cloudflare.com/client/v4/zones/{os.getenv('ID_DNS')}/dns_records/{to_delete}"
        resp2 = requests.delete(url_delete, headers=headers)
   
           
    
     