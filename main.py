import pandas as pd
import numpy as np

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.entity.entity_config import TrainingPipelineConfig, DataIngestionConfig

if __name__ == '__main__':
    logging.info("PROCEDURE: main initiated.")
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        dataingestion = DataIngestion(data_ingestion_config)
        
        data_ingestion_artifact = dataingestion.initiate_data_ingestion()

        print(data_ingestion_artifact)
        
    except Exception as e:
        raise NetworkSecurityException(e)
