import os
# from unicodedata import name
from dotenv import load_dotenv
# import shutil
a="jose"
with open('/etc/nginx/sites-available/b', 'r') as file :
  filedata = file.read()

# Replace the target stringch
filedata = filedata.replace(a, os.getenv('DOMAIN'))
filedata = filedata.replace('{{origin}}', '80')
filedata = filedata.replace('{{server_name}}', '80')
# Write the file out again
with open('/etc/nginx/sites-available/b', 'w') as file:
  file.write(filedata)



# sed -i "s/{{port}}/$PORT/g" /etc/nginx/sites-available/${NAME}
# sed -i "s/{{origin}}/$NAME/g" /etc/nginx/sites-available/${NAME}
# sed -i "s/{{server_name}}/$server/g" /etc/nginx/sites-available/${NAME}
# ln -s /etc/nginx/sites-available/${NAME} /etc/nginx/sites-enabled/${NAME}