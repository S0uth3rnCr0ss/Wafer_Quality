from pymongo.mongo_client import MongoClient
import pandas as pd
import json
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os

load_dotenv()

username = quote_plus(os.getenv("MONGO_USERNAME"))
password = quote_plus(os.getenv("MONGO_PASSWORD"))

uri = f"mongodb+srv://{username}:{password}@cluster0.148sx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri)


DATABASE_NAME = os.getenv("MONGO_DATABASE_NAME")
COLLECTION_NAME = os.getenv("waferfault")
# Read CSV
df = pd.read_csv(r"notebook\wafer_fault.csv")
df = df.drop("Unnamed: 0", axis=1)

# Convert to JSON
json_record = list(json.loads(df.T.to_json()).values())

# Remove _id if it exists
for record in json_record:
    record.pop("_id", None)

# Insert into MongoDB
try:
    client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_record)
    print("Data inserted successfully.")
except Exception as e:
    print("Error inserting data:", e)
