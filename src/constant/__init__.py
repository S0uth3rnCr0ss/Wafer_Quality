import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

AWS_S3_BUCKET_NAME = "wafer_fault"

TARGET_COLUMN = "quality"

username = quote_plus(os.getenv("MONGO_USERNAME"))
password = quote_plus(os.getenv("MONGO_PASSWORD"))

MONGO_DATABASE_NAME = os.getenv("MONGO_DATABASE_NAME")
MONGO_COLLECTION_NAME = os.getenv("MONGO_COLLECTION_NAME")

# Construct the safe URI
MONGO_DB_URL = f"mongodb+srv://{username}:{password}@cluster0.148sx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

MODEL_FILE_NAME = "model"
MODEL_FILE_EXTENSION = ".pkl"
artifact_folder = "artifacts"


