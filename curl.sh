curl -X POST "https://api.cloudflare.com/client/v4/zones/$ID_DNS/dns_records"  -H "X-Auth-Email: $EMAIL" -H "X-Auth-Key: $KEY" -H "Content-Type: application/json"  --data '{"type":"A","name":"borrar22prueab","content":"'$IP'","ttl":3600,"priority":10,"proxied":true}'
curl -X POST "https://api.cloudflare.com/client/v4/zones/00509807996f64ff48b75c82936f0777/dns_records"  -H "X-Auth-Email: $EMAIL" -H "X-Auth-Key: $KEY" -H "Content-Type: application/json"  --data '{"type":"A","name":"borrar22prueab","content":"'$IP'","ttl":3600,"priority":10,"proxied":true}'

~