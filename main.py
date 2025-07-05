import pandas as pd
import numpy as np

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer
from networksecurity.entity.entity_config import TrainingPipelineConfig, DataIngestionConfig, DataValidationConfig, DataTransformationConfig, ModelTrainerConfig

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

        data_transformation_config = DataTransformationConfig(training_pipeline_config)
        data_trasformation = DataTransformation(data_validation_artifact, data_transformation_config)

        data_transformation_artifact = data_trasformation.initiate_data_transformation()

        model_trainer_config = ModelTrainerConfig(training_pipeline_config)
        model_trainer = ModelTrainer(model_trainer_config=model_trainer_config,
                                     data_transformation_artifact=data_transformation_artifact)
        
        model_trainer_artifact = model_trainer.initiate_model_trainer()
        print(model_trainer_artifact)
        # a = np.load('Artifacts/06_30_2025_14_50_15/data_transformation/transformed/test.npy')
        # a = pd.DataFrame(a).head()
        # print(a)

    except Exception as e:
        raise NetworkSecurityException(e)
