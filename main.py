import pandas as pd
import numpy as np

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.entity.entity_config import TrainingPipelineConfig, DataIngestionConfig, DataValidationConfig

if __name__ == '__main__':
    logging.info("PROCEDURE: main initiated.")
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        dataingestion = DataIngestion(data_ingestion_config)
        
        data_ingestion_artifact = dataingestion.initiate_data_ingestion()
        
        data_validation_config = DataValidationConfig(training_pipeline_config)
        data_validation = DataValidation(data_ingestion_artifact, data_validation_config)

        data_validation_artifact = data_validation.initiate_data_validation()

        print(data_ingestion_artifact)
        
    except Exception as e:
        raise NetworkSecurityException(e)
