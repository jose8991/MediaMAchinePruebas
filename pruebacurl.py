from distutils.command.config import dump_file
import pandas as pd
import os ,json, requests
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
    # for r in respuesta["result"]:
    #     a=(r["name"][:r["name"].index(".")])
    #     list.append(a)
    # return list
    print(resp)
print(lista_dns())
# ListaDns=lista_dns()
# LocationFile=f"{os.getenv('MMHOME')}/settings/InstaPruebas.csv"
# df=pd.read_csv(LocationFile, header=None)




