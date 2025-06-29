from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.contants.training_pipeline import (TARGET_COLUMN, DATA_TRANSFORMER_IMPUTER_PARAMETERS)
from networksecurity.entity.artifact_entity import (DataValidationArtifact, DataTransformationArtifact)
from networksecurity.entity.entity_config import DataTransformationConfig
from networksecurity.utils.main_utils.utils import (save_numpy_array_data, save_object)

import os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

class DataTransformation:
    def __init__(self, data_validation_artifact:DataValidationArtifact, 
                 data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        
        except Exception as e:
            raise NetworkSecurityException(e)
        
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        """
        Purpose: To read data and return pandas DataFrame.
        Input:  file_path --> The path of the file
        Output: DataFrame --> Pandas DataFrame.
        """
        try:
            return pd.read_csv(file_path)
             
        except Exception as e:
            raise NetworkSecurityException(e)

    def get_data_transformer_object(cls):
        """
        It initialized KNNImputer object with the parameters specified in 'networksecurity/contants/training_pipeline/__init__.py'
        and returns Pipeline object with KNNImputer object as first step.

        Input/Args:
                cls: DataTransformation

        Output/Return:
                A Pipeline obj
        """
        logging.info("PROCEDURE: get_data_transformer_object from DataTransformation class, STATUS[1 of 2]: Initiated.")
        try:
            imputer:KNNImputer = KNNImputer(**DATA_TRANSFORMER_IMPUTER_PARAMETERS) # key-value pairs
            pipeline:Pipeline = Pipeline(
                [
                    ("KNNImputer", imputer)
                ]
            )
            logging.info("PROCEDURE: get_data_transformer_object from DataTransformation class, STATUS[2 of 2]: Complete.")
            return pipeline

        except Exception as e:
            raise NetworkSecurityException(e)

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        logging.info("PROCEDURE: Data Transformation, STATUS[1 of 6]: Initiated.")
        try:
            logging.info("PROCEDURE: Data Transformation, STATUS[2 of 6]: Read data from validated sets --> pd.DataFrame.")
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            # Input and Target feature training DataFrame
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            # Replace -1 with 0 in df[TARGET_COLUMN]
            target_feature_train_df.replace(-1, 0)
            
            # Input and Target feature testing DataFrame
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            # Replace -1 with 0 in df[TARGET_COLUMN]
            target_feature_test_df.replace(-1, 0)

            logging.info("PROCEDURE: Data Transformation, STATUS[3 of 6]: applying KNNImputer on input features(both train and test).")
            preprocessor = self.get_data_transformer_object()
            transformed_input_feature_train_df = preprocessor.fit_transform(input_feature_train_df)
            transformed_input_feature_test_df = preprocessor.transform(input_feature_test_df)

            # Final train and test array (used c_ for kinda concatinating)
            train_arr = np.c_[transformed_input_feature_train_df, target_feature_train_df]
            test_arr = np.c_[transformed_input_feature_test_df, target_feature_test_df]
            
            # Saving traning and test arrays (.npy file)
            logging.info("PROCEDURE: Data Tranformation, STATUS[4 of 6]: Saving train.npy and test.npy files.")
            save_numpy_array_data(file_path=self.data_transformation_config.data_transformation_train_file_path,
                                  array=train_arr)

            save_numpy_array_data(file_path=self.data_transformation_config.data_transformation_test_file_path,
                                  array=test_arr)
            # Saving preprocessor.pkl file
            logging.info("PROCEDURE: Data Tranformation, STATUS[5 of 6]: Saving preprocessor.pkl file.")
            save_object(file_path=self.data_transformation_config.data_transformation_object_file_path,
                        obj=preprocessor)
            
            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path = self.data_transformation_config.data_transformation_object_file_path,
                transformed_train_file_path = self.data_transformation_config.data_transformation_train_file_path,
                transformed_test_file_path = self.data_transformation_config.data_transformation_test_file_path
                )
            
            logging.info("PROCEDURE: Data Tranformation, STATUS[6 of 6]: Complete.")
            return data_transformation_artifact

        except Exception as e:
            raise NetworkSecurityException(e)
