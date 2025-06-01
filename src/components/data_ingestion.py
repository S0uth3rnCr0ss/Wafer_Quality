import sys
import os 
import numpy as np
import pandas as pd
from pymongo import MongoClient
from zipfile import Path
from src.constant import *
from src.exceptions import CustomException
from src.utils.main_utils import MainUtils
from dataclasses import dataclass
from src.logger import logging



@dataclass
class DataIngestionConfig:
    artifact_folder: str = os.path.join(artifact_folder)
    
class DataIngestion:
    def __init__(self) -> None:
        self.data_ingestion_config = DataIngestionConfig()
        self.utils = MainUtils()
        
    def export_collection_as_dataframe(self, collection_name, db_name):
        # Connection to the database
        try:
            mongo_client = MongoClient(MONGO_DB_URL)
            
            collection = mongo_client[db_name][collection_name]
            
            df = pd.DataFrame(list(collection.find()))
            
            if "Unnamed: 0" in df.columns:
                df.drop('Unnamed: 0', axis=1, inplace=True)
                
            if "_id" in df.columns.to_list():
                df = df.drop(columns = ['_id'], axis=1)
                
            df.replace({'na':np.nan}, inplace=True)
            
            return df
        except Exception as e:
            raise CustomException(e, sys)
        
        
    # Function to store data
    def export_data_into_feature_store_file_path(self) -> pd.DataFrame:
        try:
            logging.info("Exporting data from mongo")
            raw_file_path = self.data_ingestion_config.artifact_folder
            
            os.makedirs(raw_file_path, exist_ok=True)
            
            sensor_data = self.export_collection_as_dataframe(
                collection_name = MONGO_COLLECTION_NAME,
                db_name = MONGO_DATABASE_NAME,   # Stores data in pd dataframe
            )
            
            
            logging.info(f"saving exported data into feature store file path: {raw_file_path}")
            
            feature_store_file_path = os.path.join(raw_file_path, 'wafer_fault.csv')
            
            #Storing data to csv
            sensor_data.to_csv(feature_store_file_path, index=False)
            
            return feature_store_file_path
        
        except Exception as e:
            raise CustomException(e, sys)
        
        
    # Function to call all the above functions 
    def initiate_data_ingestion(self) -> Path:
        
        logging.info("Enter initiated_data_igestion method of data_integration")
        
        try:
            feature_store_file = self.export_data_into_feature_store_file_path()
            
            logging.info("Successfully got the data from Mongodb")
            
            logging.info("Stored CSV file in the following path")
            
            return feature_store_file
            
        except Exception as e:
            raise CustomException(e, sys)