import os

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer

from networksecurity.contants.training_pipeline import TRAINING_BUCKET_NAME

from networksecurity.cloud.s3_syncer import S3Sync

from networksecurity.entity.entity_config import (
    TrainingPipelineConfig,
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig
)

from networksecurity.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact,
    ModelTrainerArtifact
)

class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()
        self.s3_sync = S3Sync()

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

            return data_ingestion_artifact
        
        except Exception as e:
            raise NetworkSecurityException(e)
        
    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            data_validation_config = DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            data_validation = DataValidation(data_ingestion_artifact=self.initiate_data_ingestion(),
                                             data_validation_config=data_validation_config)
            
            data_validation_artifact = data_validation.initiate_data_validation()

            return data_validation_artifact
        
        except Exception as e:
            raise NetworkSecurityException(e)
        
    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            data_transformation_config = DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            data_transformation = DataTransformation(data_validation_artifact=self.initiate_data_validation(),
                                                     data_transformation_config=data_transformation_config)
            
            data_transformation_artifact = data_transformation.initiate_data_transformation()

            return data_transformation_artifact

        except Exception as e:
            raise NetworkSecurityException(e)
        
    def initiate_model_training(self) -> ModelTrainerArtifact:
        try:
            model_training_config = ModelTrainerConfig(training_pipeline_config=self.training_pipeline_config)
            model_trainer = ModelTrainer(data_transformation_artifact=self.initiate_data_transformation(),
                                         model_trainer_config=model_training_config)
            
            model_trainer_artifact = model_trainer.initiate_model_trainer()

            return model_trainer_artifact

        except Exception as e:
            raise NetworkSecurityException(e)
        
    # Local Artifact --> S3
    def sync_artifact_dir_to_s3(self):
        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/artifact/{self.training_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder=self.training_pipeline_config.artifact_dir, aws_bucket_url=aws_bucket_url)

        except Exception as e:
            raise NetworkSecurityException(e)

    # Local final model --> S3    
    def sync_saved_model_to_s3(self):
        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/final_model/{self.training_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder=self.training_pipeline_config.model_dir, aws_bucket_url=aws_bucket_url)

        except Exception as e:
            raise NetworkSecurityException(e)


    def run_pipeline(self):
        try:
            """
            Note:
            The three steps below are commented out because `self.initiate_model_training()` internally calls them.
            Uncomment them if you want to execute or debug each step individually.
            """
            # data_ingestion_artifact = self.initiate_data_ingestion()
            # data_validation_artifact = self.initiate_data_validation()
            # data_transformation_artifact = self.initiate_data_transformation()
            model_trainer_artifact = self.initiate_model_training()

            self.sync_artifact_dir_to_s3()
            self.sync_saved_model_to_s3()

            return model_trainer_artifact

        except Exception as e:
            raise NetworkSecurityException(e)