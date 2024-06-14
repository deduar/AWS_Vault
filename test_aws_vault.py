import os
from pymongo import MongoClient
import hvac
from dotenv import load_dotenv

load_dotenv()

VAULT_HOST = os.getenv('VAULT_HOST')
VAULT_TOKEN = os.getenv('VAULT_TOKEN')

client = hvac.Client(
    url=VAULT_HOST,
    token=VAULT_TOKEN,
)

res = client.secrets.kv.v2.read_secret(
    path='cling-dev/cling/common', mount_point='coinscrap-dev')

MONGO_URI = res["data"]["data"]["MONGO_URI"]

connection = MongoClient(MONGO_URI)
DB = connection.list_database_names()
print(connection[DB[0]][connection[DB[0]].list_collection_names()[15]].
      find_one({"$and": [
          {"documentUrl": {"$ne": None}},
          {"predictions.categorization.category": {"$eq": "seguros"}}]}))
connection.close()
