import sys 
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.constant import *
from src.exceptions import CustomException
from src.logger import logging
from src.utils.main_utils import MainUtils
from dataclasses import dataclass

@dataclass
class DataTransformationConfig:
    artifact_dir = os.path.join(artifact_folder)
    transformed_train_file_path = os.path.join(artifact_dir,'train.npy')
    transformed_test_file_path = os.path.join(artifact_dir,'test.npy')
    transformed_object_file_path = os.path.join(artifact_dir,'preprocessor.pkl')
    
    
class DataTransformation:
    def __init__(self, feature_store_file_path):
        self.feature_store_file_path = feature_store_file_path
        self.data_transformation_config = DataTransformationConfig()
        self.utils = MainUtils()
        
    @staticmethod
    def get_data(feature_store_file_path: str) -> pd.DataFrame:
        try:
            data = pd.read_csv(feature_store_file_path)
            
            data.rename(columns={"Good/Bad": TARGET_COLUMN}, inplace=True)
            
            return data
        
        except Exception as e:
            raise CustomException(e, sys)
        
    def get_data_transformer_object(self):
        
        try:
            imputer_step = ('imputer', SimpleImputer(strategy='constant', fill_value=0))
            scaler_step = ('scaler', RobustScaler())
            
            preprocessor = Pipeline(
                steps=[
                    imputer_step, 
                    scaler_step
                ]
            )
            return preprocessor
        
        except Exception as e:
            raise CustomException(e, sys)
    
    def initiate_data_transformation(self):
        logging.info("Entered initiate_data_transformation method of data transformation class")
    
        try:
            # Load data
            dataframe = self.get_data(feature_store_file_path=self.feature_store_file_path)
            
            # Separate features and target
            X = dataframe.drop(columns=TARGET_COLUMN)
            
            # Fix here: use correct syntax for filtering target values
            # Assuming you want to keep only rows where target is -1, 0, or 1:
            mask = dataframe[TARGET_COLUMN].isin([-1, 0, 1])
            y = dataframe.loc[mask, TARGET_COLUMN]
            X = X.loc[mask]
            
            # Train-test split
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
            
            # Get preprocessing object and fit-transform train data, transform test data
            preprocessor = self.get_data_transformer_object()
            
            X_train_scaled = preprocessor.fit_transform(X_train)
            X_test_scaled = preprocessor.transform(X_test)
            
            # Save preprocessor object path
            preprocessor_path = self.data_transformation_config.transformed_object_file_path
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(preprocessor_path), exist_ok=True)
            
            # Save the preprocessor
            self.utils.save_object(file_path=preprocessor_path, obj=preprocessor)
            
            # Combine scaled features and target arrays
            train_arr = np.c_[X_train_scaled, np.array(y_train)]
            test_arr = np.c_[X_test_scaled, np.array(y_test)]
            
            return train_arr, test_arr, preprocessor_path

        except Exception as e:
            raise CustomException(e, sys)

