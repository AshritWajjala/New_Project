from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException

from networksecurity.entity.entity_config import ModelTrainerConfig
from networksecurity.entity.artifact_entity import  DataTransformationArtifact, ModelTrainerArtifact, ClassificationMetricArtifact

from networksecurity.utils.ml_utils.model.model_utils import NetworkModel
from networksecurity.utils.main_utils.utils import save_object, load_object
from networksecurity.utils.main_utils.utils import load_numpy_array_data
from networksecurity.utils.main_utils.utils import evaluate_models

from networksecurity.contants.training_pipeline import MODELS, MODEL_PARAMS

import os
import mlflow
import dagshub
import joblib

dagshub.init(repo_owner='AshritWajjala', repo_name='New_Project', mlflow=True)

class ModelTrainer:
    def __init__(self, model_trainer_config:ModelTrainerConfig, data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact

        except Exception as e:
            raise NetworkSecurityException(e)
        
    def track_mlflow(self, best_model, classification_metrics:object) -> None:
        mlflow.set_experiment("network_security_experiment")

        with mlflow.start_run():
            f1_score = classification_metrics.f1_score
            precision_score = classification_metrics.precision_score
            recall_score = classification_metrics.recall_score

            mlflow.log_metric("f1_score", f1_score)
            mlflow.log_metric("precision_score", precision_score)
            mlflow.log_metric("recall score", recall_score)
            joblib.dump(best_model, "best_model.joblib") # Better than pickle. Used to save model objects
            mlflow.log_artifact("best_model.joblib") # Dagshub no longer supports sklearn.log_model
            

    def training_and_evaluation(self, X_train, y_train, X_test, y_test):
        try:
            model_report = evaluate_models(X_train=X_train,
                                           X_test=X_test, 
                                           y_train=y_train,
                                           y_test=y_test, 
                                           MODELS=MODELS,
                                           MODEL_PARAMS=MODEL_PARAMS)

            # Best model, model_name, model_score
            best_model_name = max(model_report, key=lambda name: model_report[name]['metrics']['test_f1_score'])
            best_model = model_report[best_model_name]['model_object']

            # Model metrics with respect to training data (check the presence of overfitting)
            best_model_train_f1_score = model_report[best_model_name]['metrics']['train_f1_score']
            best_model_train_precision_score = model_report[best_model_name]['metrics']['train_precision_score']
            best_model_train_recall_score = model_report[best_model_name]['metrics']['train_recall_score']

            # Model metrics with respect to testing data
            best_model_test_f1_score = model_report[best_model_name]['metrics']['test_f1_score']
            best_model_test_precision_score = model_report[best_model_name]['metrics']['test_precision_score']
            best_model_test_recall_score = model_report[best_model_name]['metrics']['test_recall_score']

            # Creating directory to save model.pkl
            model_file_path = self.model_trainer_config.trained_model_file_path
            model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(model_dir_path, exist_ok=True)

            save_object(file_path=model_file_path, obj=best_model)
            save_object(file_path="final_model/model.pkl", obj=best_model)

            # Artifacts for best model
            train_metric_artifact = ClassificationMetricArtifact(
                f1_score=best_model_train_f1_score,
                precision_score=best_model_train_precision_score,
                recall_score=best_model_train_recall_score
            )

            test_metric_artifact = ClassificationMetricArtifact(
                f1_score=best_model_test_f1_score,
                precision_score=best_model_test_precision_score,
                recall_score=best_model_test_recall_score
            )

            model_trainer_artifact = ModelTrainerArtifact(
                train_metric_artifact=train_metric_artifact,
                test_metric_artifact=test_metric_artifact,
                trained_model_file_path=model_file_path
            )

            # Track MLFLOW
            self.track_mlflow(best_model=best_model, classification_metrics=train_metric_artifact)
            self.track_mlflow(best_model=best_model, classification_metrics=test_metric_artifact)

            return model_trainer_artifact

        except Exception as e:
            raise NetworkSecurityException(e)

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            logging.info("PROCEDURE: Model Training and Evaluation, STATUS[1 of ]: Initiated.")
            # File paths of 
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)

            X_train, X_test, y_train, y_test = (
                train_arr[:,:-1],
                test_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,-1]
            )
            
            model_trainer_artifact = self.training_and_evaluation(X_train, y_train, X_test, y_test)
            logging.info("PROCEDURE: Model Training and Evaluation, STATUS[]: Complete")

            return model_trainer_artifact


        except Exception as e:
            raise NetworkSecurityException(e)