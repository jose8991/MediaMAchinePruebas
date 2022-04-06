from distutils.command.config import dump_file
import pandas as pd
import os ,json, requests
from requests.structures import CaseInsensitiveDict
from dotenv import load_dotenv

#call the cloudflare api with your credentials
url = f"https://api.cloudflare.com/client/v4/zones/{os.getenv('ID_DNS')}/dns_records"
headers = CaseInsensitiveDict()
headers["X-Auth-Email"] = os.getenv('EMAIL')
headers["X-Auth-Key"] = os.getenv('KEY')
headers["Content-Type"] = "application/json"

#we extract the json from the existing cloudflare dns
resp = requests.get(url, headers=headers)
respuesta=json.loads(resp.text)
dns_dict={}
#We store the name of the subdomain in a dictionary as a key and the id that represents it as a value
for r in respuesta["result"]:
    a=r["name"].split(".",1)[0]
    dns_dict[a]=r["id"]

    
#we read the csv that we want to review and put it in a list that contains the values ​​of the second row
locationFile=f"{os.getenv('MMHOME')}/settings/insta_wp_map.csv"
df=pd.read_csv(locationFile, header=None)
elementListCsv=df[1].values

#we loop through the dictionary and check if it exists in the elementListCsv and if it exists in the nginx path
#if it does not exist in any of the two delete it
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
   
           
    
     