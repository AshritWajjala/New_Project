from datetime import datetime
import os
import numpy as np
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import (RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier)
from xgboost import XGBClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

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

TRAINING_BUCKET_NAME: str = "ml-networksecurity"

SCHEMA_FILE_PATH: str = os.path.join("data_schema", "schema.yaml")

MODELS:dict = {
    "Decision Tree": DecisionTreeClassifier(),
    "Random Forest": RandomForestClassifier(verbose=1),
    "Gradient Boosting": GradientBoostingClassifier(verbose=1),
    "Logistic Regression": LogisticRegression(verbose=1),
    "AdaBoost": AdaBoostClassifier(),
    "XGBoost": XGBClassifier(),
    "KNN": KNeighborsClassifier()
}

MODEL_PARAMS:dict = {
            "Decision Tree": {
                'criterion':['gini', 'entropy', 'log_loss'],
                # 'splitter':['best','random'],
                # 'max_features':['sqrt','log2'],
            },
            "Random Forest":{
                # 'criterion':['gini', 'entropy', 'log_loss'],
                
                # 'max_features':['sqrt','log2',None],
                'n_estimators': [8,16,32,128,256]
            },
            "Gradient Boosting":{
                # 'loss':['log_loss', 'exponential'],
                'learning_rate':[.1,.01,.05,.001],
                'subsample':[0.6,0.7,0.75,0.85,0.9],
                # 'criterion':['squared_error', 'friedman_mse'],
                # 'max_features':['auto','sqrt','log2'],
                'n_estimators': [8,16,32,64,128,256]
            },
            "Logistic Regression":{},
            "AdaBoost":{
                'learning_rate':[.1,.01,.001],
                'n_estimators': [8,16,32,64,128,256]
            },
            "XGBoost":{},
            "KNN": {
                "weights": ['uniform', 'distance'],
                "algorithm": ['auto', 'ball_tree', 'kd_tree']
            }
            
        }


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

"""
Contants that are related to MODEL TRAINER procedure starts with 'MODEL_TRAINER_'
"""
MODEL_TRAINER_DIR_NAME:str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR:str = "trained_model"
MODEL_TRAINER_MODEL_FILE_NAME:str = "model.pkl"
MODEL_TRAINER_EXPECTED_SCORE:float = 0.0
MODEL_TRAINER_OVERFITTING_UNDERFITTING_THRESHOLD:float = 0.05