#curl -X GET "https://api.cloudflare.com/client/v4/zones/$ID_DNS/dns_records"      -H "X-Auth-Email: $EMAIL"      -H "X-Auth-Key: $KEY"      -H "Content-Type: application/json" | jq > dns.jsonimport requests
import requests
import json
from requests.structures import CaseInsensitiveDict

url = "https://api.cloudflare.com/client/v4/zones/00509807996f64ff48b75c82936f0777/dns_records"

headers = CaseInsensitiveDict()
headers["X-Auth-Email"] = "pruebaoraclecloud@gmail.com"
headers["X-Auth-Key"] = "3cffda0574248ed95108e39e89a37c75dfba6"
headers["Content-Type"] = "application/json"


resp = requests.get(url, headers=headers)
respuesta=json.loads(resp.text)
for r in respuesta["result"]:
    print(r["name"])
    print(r["name"][:r["name"].index(".")])
#print(resp.text)
# url = "https://api.cloudflare.com/client/v4/zones/00509807996f64ff48b75c82936f0777/dns_records"

# headers = CaseInsensitiveDict()
# headers["X-Auth-Email"] = "pruebaoraclecloud@gmail.com"
# headers["X-Auth-Key"] = "3cffda0574248ed95108e39e89a37c75dfba6"
# headers["Content-Type"] = "application/json"