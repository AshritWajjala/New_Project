from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.entity.entity_config import DataValidationConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from networksecurity.contants.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils.main_utils.utils import read_yaml_file, write_yaml_file

import os
import pandas as pd
from typing import Any
from scipy.stats import ks_2samp # To check Data Drift

class DataValidation:
    def __init__(self, data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_config:DataValidationConfig) -> None:
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
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
        
    def validate_no_of_columns(self, dataframe:pd.DataFrame) -> bool:
        try:
            no_of_columns = len(self._schema_config)
            logging.info(f"Number of columns required: {no_of_columns}")
            logging.info(f"Number of columns in dataframe: {len(dataframe.columns)}")
            return True if no_of_columns == len(dataframe.columns) else False
        except Exception as e:
            raise NetworkSecurityException(e)
        
    def validate_numerical_columns(self, dataframe:pd.DataFrame) -> bool:
        try:
            expected = self._schema_config.get('numerical_columns', [])
            actual = dataframe.select_dtypes(exclude='object').columns.to_list()
            logging.info(f"Number of numerical columns required: {len(expected)}")
            logging.info(f"Number of numerical columns in dataframe: {len(actual)}")
            return set(expected) == set(actual)        
        
        except Exception as e:
            raise NetworkSecurityException(e)
        
    def detect_data_drift(self, base_df:pd.DataFrame, current_df:pd.DataFrame, threshold=0.05) -> bool:
        try:
            status = True
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                has_same_dist: Any = ks_2samp(d1, d2) # Remove Any --> Pylance error (at .pvalue)
                if threshold < has_same_dist.pvalue:
                    is_found = False
                else:
                    is_found = True
                    status = False
                
                # Updating report
                report.update({
                    column:{
                        "p-value": float(has_same_dist.pvalue),
                        "drift_status": is_found
                    }
                })

            drift_report_file_path = self.data_validation_config.drift_report_file_path

            # Creating directory
            dir = os.path.dirname(drift_report_file_path)
            os.makedirs(dir, exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path,
                            content=report)
            
            return status
        
        except Exception as e:
            raise NetworkSecurityException(e)


    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            logging.info("PROCEDURE: Data Validation, STATUS[1 of 6]: Initiated.")
            train_file_path = self.data_ingestion_artifact.training_file_path
            test_file_path = self.data_ingestion_artifact.testing_file_path
            
            logging.info("PROCEDURE: Data Validation, STATUS[2 of 6]: Reaing data from train and test file path.")
            # Read data from train and test file path
            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_file_path)

            logging.info("PROCEDURE: Data Validation, STATUS[3 of 6]: Validating number of columns.")
            # Validate number of columns
            train_status = self.validate_no_of_columns(dataframe=train_dataframe)
            if not train_status:
                error_message = "Columns missing in Training DataFrame."
            test_status = self.validate_no_of_columns(dataframe=test_dataframe)
            if not test_status:
                error_message = "Columns missing in Training DataFrame."

            logging.info("PROCEDURE: Data Validation, STATUS[4 of 6]: Validating numerical columns.")
            # Validate numerical columns
            train_status = self.validate_numerical_columns(dataframe=train_dataframe)
            if not train_status:
                error_message = "Numerical Columns missing in Training DataFrame."
            test_status = self.validate_numerical_columns(dataframe=test_dataframe)
            if not test_status:
                error_message = "Numerical Columns missing in Training DataFrame."

            logging.info("PROCEDURE: Data Validation, STATUS[5 of 6]: Checking for Data Drift.")
            # Checking Data Drift
            detection_status = self.detect_data_drift(base_df=train_dataframe, current_df=test_dataframe)
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path, exist_ok=True)
            if detection_status:

                train_dataframe.to_csv(
                    self.data_validation_config.valid_train_file_path, index=False, header=True
                )
                test_dataframe.to_csv(
                    self.data_validation_config.valid_test_file_path, index=False, header=True
                )

            data_validation_artifact = DataValidationArtifact(
                validation_status=detection_status,
                valid_train_file_path=self.data_validation_config.valid_test_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )

            logging.info("PROCEDURE: Data Validation, STATUS[6 of 6]: Complete.")
            return data_validation_artifact

        except Exception as e:
            raise NetworkSecurityException(e)