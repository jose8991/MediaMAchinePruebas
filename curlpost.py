import requests
from requests.structures import CaseInsensitiveDict

url = "https://api.cloudflare.com/client/v4/zones/00509807996f64ff48b75c82936f0777/dns_records"

headers = CaseInsensitiveDict()
headers["X-Auth-Email"] = "pruebaoraclecloud@gmail.com"
headers["X-Auth-Key"] = "3cffda0574248ed95108e39e89a37c75dfba6"
headers["Content-Type"] = "application/json"

data = '{"type":"A","name":"pruebadesdepython","content":"54.208.136.12","ttl":3600,"priority":10,"proxied":true}'


resp = requests.post(url, headers=headers, data=data)

print(resp.status_code)
