import yaml
import os
import numpy as np
import dill
import pickle

from sklearn.model_selection import GridSearchCV

from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.contants.training_pipeline import MODELS, MODEL_PARAMS
from networksecurity.utils.ml_utils.classification_metric_utils.utils import get_classification_score
from networksecurity.utils.ml_utils.model.model_utils import NetworkModel

def read_yaml_file(file_path: str) -> dict:
    """
    This function is used to read the content of the yaml file.
    Input:  file_path --> The path of the yaml file.

    Output: dict --> Dictionary of content.
    """
    try:
        with open(file_path, 'rb') as f:
            return yaml.safe_load(f)
        
    except Exception as e:
        raise NetworkSecurityException(e)
    
def write_yaml_file(file_path:str, content:object, replace:bool = False) -> None:
    """
    This function is used to write content into a yaml file.
    Input:  file_path --> The path of the file.
            content --> The content that needs to be written.
            Replace --> True if path exists and need to be replaced
    
    Output: None
    """
    try:
        # In case the file need to be replaced (if existing)
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        else:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Writing 
        with open(file_path, 'w') as f:
            yaml.dump(content, f)

    except Exception as e:
        raise NetworkSecurityException(e)
    
def save_numpy_array_data(file_path:str, array:np.array): 
    """
    This method saves numpy array data to file (.npy file)
    Input:  array --> The numpy array from which the data needs to be transferred.
            file_path --> The path of the file where the data needs to be transferred.
    """
    try:
        logging.info("PROCEDURE: Executing 'save_numpy_array_data' method, STATUS: Initiated.")
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as f:
            np.save(f, array)
        logging.info("PROCEDURE: Executing 'save_numpy_array_data' method, STATUS: Complete.")

    except Exception as e:
        raise NetworkSecurityException(e)
    
def load_numpy_array_data(file_path:str) -> np.array:
    """
    This method load numpy array data from the file (.npy file)
    Input:  file_path --> The path of the file from which the array needs to be retrieved.
    """
    try:
        logging.info("PROCEDURE: Executing 'load_numpy_array_data' method, STATUS: Initiated.")
        with open(file_path, 'rb') as f:
            array = np.load(f)
        logging.info("PROCEDURE: Executing 'load_numpy_array_data' method, STATUS: Complete.")

        return array

    except Exception as e:
        raise NetworkSecurityException(e)
    
def save_object(file_path:str, obj:object) -> None:
    """
    This function is used to store the object in the file_path in .pkl file extension.
    Input:  file_path --> The path of the .pkl file
            obj --> object that needs to be stored in .pkl file.
    """
    try:
        logging.info("PROCEDURE: Executing 'Save object' method, STATUS: Initiated.")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as f:
            pickle.dump(obj, f)
        logging.info("PROCEDURE: Executing 'Save object' method, STATUS: Complete.")
    
    except Exception as e:
        raise NetworkSecurityException(e)
    
def load_object(file_path:str) -> None:
    """
    This function is used to load the object that is saved in the file_path in .pkl file extension.
    Input:  file_path --> The path of the .pkl file
    """
    try:
        logging.info("PROCEDURE: Executing 'Load object' method, STATUS: Initiated.")
        with open(file_path, 'rb') as f:
            obj = pickle.load(f)
        logging.info("PROCEDURE: Executing 'Load object' method, STATUS: Complete.")

        return obj
    
    except Exception as e:
        raise NetworkSecurityException(e)
    
from sklearn.model_selection import GridSearchCV
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.utils.main_utils.utils import get_classification_score

def evaluate_models(X_train, X_test, y_train, y_test, MODELS, MODEL_PARAMS):
    """
    Purpose: Evaluate multiple models with hyperparameter tuning and return their performance metrics.

    Returns:
        report (dict): {
            "ModelName": {
                "y_train_pred": [...],
                "y_test_pred": [...],
                "metrics": {
                    ...
                }
            }
        }
    """
    try:
        logging.info("\n==================== MODEL EVALUATION INITIATED ====================")
        report = {}

        for model_name, model in MODELS.items():
            logging.info(f"\n[START] Processing model: {model_name}")
            param_grid = MODEL_PARAMS.get(model_name, {})
            logging.info(f"Hyperparameter grid for {model_name}: {param_grid if param_grid else 'Default (no tuning)'}")

            # Grid Search for best hyperparameters
            grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=3, n_jobs=-1, verbose=0)
            grid_search.fit(X_train, y_train)
            logging.info(f"✔ GridSearchCV completed for {model_name}")
            
            best_model = grid_search.best_estimator_
            logging.info(f"🏆 Best hyperparameters for {model_name}: {grid_search.best_params_}")

            # Train best model again (redundant but ensures correct state)
            best_model.fit(X_train, y_train)
            logging.info(f"✔ {model_name} trained with best parameters.")

            # Predictions
            y_train_pred = best_model.predict(X_train)
            y_test_pred = best_model.predict(X_test)

            # Evaluation metrics
            train_classification_metrics = get_classification_score(y_test=y_train, y_pred=y_train_pred)
            test_classification_metrics = get_classification_score(y_test=y_test, y_pred=y_test_pred)

            logging.info(f"📊 Performance for {model_name}:")
            logging.info(f"    - Train F1 Score: {train_classification_metrics.f1_score:.4f}")
            logging.info(f"    - Test F1 Score : {test_classification_metrics.f1_score:.4f}")

            # Save to report
            report[model_name] = {
                "y_train_pred": y_train_pred,
                "y_test_pred": y_test_pred,
                "model_object": best_model, 
                "metrics": {
                    "train_f1_score": train_classification_metrics.f1_score,
                    "train_precision_score": train_classification_metrics.precision_score,
                    "train_recall_score": train_classification_metrics.recall_score,
                    "test_f1_score": test_classification_metrics.f1_score,
                    "test_precision_score": test_classification_metrics.precision_score,
                    "test_recall_score": test_classification_metrics.recall_score
                }
            }

            logging.info(f"[END] Evaluation complete for {model_name}.\n{'-'*65}")

        logging.info("==================== MODEL EVALUATION COMPLETE ====================\n")
        return report

    except Exception as e:
        logging.error("❌ Exception occurred during model evaluation.")
        raise NetworkSecurityException(e)



    