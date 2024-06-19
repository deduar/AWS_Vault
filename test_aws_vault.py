import os
import re
import hvac
import pandas as pd
import difflib

from dotenv import load_dotenv
from pymongo import MongoClient

# Read secret to connect
load_dotenv()
VAULT_HOST = os.getenv('VAULT_HOST')
VAULT_TOKEN = os.getenv('VAULT_TOKEN')
client = hvac.Client(
    url=VAULT_HOST,
    token=VAULT_TOKEN,
)

res = client.secrets.kv.v2.read_secret(
    path='evo-ahorro-prd/evo-ahorro/common', mount_point='coinscrap-prd')
MONGO_URI = res["data"]["data"]["MONGO_URI"]

# Connect documentDB
connection = MongoClient(MONGO_URI)
DB = connection.list_database_names()

# Read CSV ein pandas and firt loop (ESK code -IN-> EVO)
df = pd.read_csv('./Data/BD_WOOWBE-Cashback.csv')
for i,row in df.iterrows():
    business = row['business']
    sector = row['sector']
    code = row['code']
    latitud = row['latitud']
    longitud = row['longitud']
    formatted_address = row['formatted_address']
    dir_limpia = row['dir_limpia']
    cif = row['cif']
    nombre = row['nombre']
    nombre_sin_punto = row['nombre_sin_punto']
    tipo_estab = row['tipo_estab']
    point_of_sale_uuid = row['point_of_sale_uuid']
    business_uuid = row['business_uuid']  

    rgx = re.compile('.*'+code+'.*', re.IGNORECASE)    
    j = connection['coinscrap']['fs_Merchant'].find({'code':rgx})
    for doc in list(j):
        # print(f"{business.lower()},{doc['name'].lower()},{difflib.SequenceMatcher(a=business.lower(), b=doc['name'].lower()).ratio()}")
        if difflib.SequenceMatcher(a=business.lower(), b=doc['name'].lower()).ratio() > 0.50:
            print(f"{business},{sector},{code},{latitud},{longitud},{formatted_address},{dir_limpia},{cif},{nombre},{nombre_sin_punto},{tipo_estab},{point_of_sale_uuid},{business_uuid},{doc['city'] if 'city' in doc else 'ana'},{doc['country'] if 'country' in doc else 'nan'},{doc['code']},'{doc['name']}'")    

connection.close()
