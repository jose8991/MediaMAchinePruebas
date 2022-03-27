import os
# from unicodedata import name
from dotenv import load_dotenv
# import shutil
a="jose"
NAME="PRUEBA"
with open('/etc/nginx/sites-available/origin', 'r') as file :
  filedata = file.read()

# Replace the target stringch
filedata = filedata.replace('{{port}}', os.getenv('DOMAIN'))
filedata = filedata.replace('{{origin}}', '80')
filedata = filedata.replace('{{server_name}}', 'prueba')
# Write the file out again
with open('/etc/nginx/sites-available/origin', 'w') as file:
  file.write(filedata)

a=(f'/etc/nginx/sites-available/{NAME}')
print(a)


# sed -i "s/{{port}}/$PORT/g" /etc/nginx/sites-available/${NAME}
# sed -i "s/{{origin}}/$NAME/g" /etc/nginx/sites-available/${NAME}
# sed -i "s/{{server_name}}/$server/g" /etc/nginx/sites-available/${NAME}
# ln -s /etc/nginx/sites-available/${NAME} /etc/nginx/sites-enabled/${NAME}