from datetime import datetime
import os
import numpy as np
import pandas as pd


"""
Defining contants for training pipeline
"""

TARGET_COLUMN: str = "Result"
PIPELINE_NAME: str = "NetworkSecurity"
ARTIFACT_DIR: str = "Artifacts"
FILE_NAME: str = "phishingData.csv"

TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"
PREPROCESSING_OBJECT_FILE_NAME = "preprocessing.pkl"

SCHEMA_FILE_PATH: str = os.path.join("data_schema", "schema.yaml")


"""
Contants that are related to DATA INGESTION procedure starts with 'DATA_INGESTION_'
"""
DATA_INGESTION_COLLECTION_NAME: str = "NetworkData"
DATA_INGESTION_DATABASE_NAME: str = "ML_AI_Journey"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2

"""
Contants that are related to DATA VALIDATION procedure starts with 'DATA_VALIDATION_'
"""
DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_VALID_DIR: str = "validated"
DATA_VALIDATION_INVALID_DIR: str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR: str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = "report.yaml"

"""
Contants that are related to DATA TRANSFORMATION procedure starts with 'DATA_TRANSFORMATION_'
"""
DATA_TRANSFORMATION_DIR_NAME:str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR:str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR:str = "transformed_object"
DATA_TRANSFORMER_IMPUTER_PARAMETERS:dict = {
    "missing_values": np.nan,
    "n_neighbors": 3,
    "weights": "uniform"
} # KNN Imputer --> used to replace NaN values.
