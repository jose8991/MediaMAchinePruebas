import os
from dotenv import load_dotenv
load_dotenv()
# una vez cargados los valores, podemos usarlos
WP_DB_HOST = os.getenv('WP_DB_HOST')

print (os.getenv('KEY'))