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
    def __init__(self, data_validation_artifact: DataValidationArtifact, 
                 data_transformation_config: DataTransformationConfig):
        try:
            logging.info("📦 [INIT] Initializing DataTransformation class...")
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
            logging.info("✅ [INIT] DataTransformation class initialized successfully.")
        except Exception as e:
            logging.error("❌ [INIT ERROR] Failed to initialize DataTransformation.")
            raise NetworkSecurityException(e)
        
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        """
        Reads data from a file and returns it as a pandas DataFrame.
        """
        try:
            logging.info(f"📄 Reading data from: {file_path}")
            df = pd.read_csv(file_path)
            logging.info(f"✅ Data read successfully with shape: {df.shape}")
            return df
        except Exception as e:
            logging.error(f"❌ Failed to read data from: {file_path}")
            raise NetworkSecurityException(e)

    def get_data_transformer_object(self):
        """
        Initializes a KNNImputer and wraps it in a Pipeline.
        """
        logging.info("🔧 [1/2] Creating data transformer pipeline using KNNImputer...")
        try:
            imputer = KNNImputer(**DATA_TRANSFORMER_IMPUTER_PARAMETERS)
            pipeline = Pipeline([("KNNImputer", imputer)])
            logging.info("✅ [2/2] Data transformer pipeline created successfully.")
            return pipeline
        except Exception as e:
            logging.error("❌ Failed to create data transformer pipeline.")
            raise NetworkSecurityException(e)

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        logging.info("\n🚀 === INITIATING DATA TRANSFORMATION PIPELINE ===")
        try:
            # Step 1: Read the data
            train_df = self.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = self.read_data(self.data_validation_artifact.valid_test_file_path)

            # Step 2: Split into input and target
            logging.info("🔍 Splitting data into input features and target column...")
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df.replace(-1, 0, inplace=True)

            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df.replace(-1, 0, inplace=True)

            # Step 3: Apply transformation
            logging.info("🔄 Applying KNNImputer transformation on training and test data...")
            preprocessor = self.get_data_transformer_object()
            transformed_input_feature_train_df = preprocessor.fit_transform(input_feature_train_df)
            transformed_input_feature_test_df = preprocessor.transform(input_feature_test_df)

            # Step 4: Concatenate input and target
            logging.info("📐 Combining transformed input with target feature...")
            train_arr = np.c_[transformed_input_feature_train_df, target_feature_train_df]
            test_arr = np.c_[transformed_input_feature_test_df, target_feature_test_df]

            # Step 5: Save .npy files
            logging.info("💾 Saving transformed training and testing data as .npy files...")
            save_numpy_array_data(self.data_transformation_config.data_transformation_train_file_path, train_arr)
            save_numpy_array_data(self.data_transformation_config.data_transformation_test_file_path, test_arr)

            # Step 6: Save transformation object
            logging.info("💾 Saving preprocessor pipeline object as preprocessor.pkl...")
            save_object(self.data_transformation_config.data_transformation_object_file_path, preprocessor)
            save_object(file_path="final_model/preprocessor.pkl", obj=preprocessor)

            # Step 7: Create and return the artifact
            logging.info("📦 Creating DataTransformationArtifact...")
            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.data_transformation_object_file_path,
                transformed_train_file_path=self.data_transformation_config.data_transformation_train_file_path,
                transformed_test_file_path=self.data_transformation_config.data_transformation_test_file_path
            )

            logging.info("✅ === DATA TRANSFORMATION COMPLETE ===\n")
            return data_transformation_artifact

        except Exception as e:
            logging.error("❌ Data Transformation failed.")
            raise NetworkSecurityException(e)
