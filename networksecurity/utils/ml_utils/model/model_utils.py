from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.contants.training_pipeline import MODELS, MODEL_PARAMS

from sklearn.model_selection import GridSearchCV

import os

class NetworkModel:
    def __init__(self, preprocessor, model):
        try:
            logging.info("PROCEDURE: Preprocessor and Model Assignment, STATUS[1 of 2]: Initiated.")
            self.preprocessor = preprocessor
            self.model = model
            logging.info("PROCEDURE: Preprocessor and Model Assignment, STATUS[2 of 2]: Complete.")
        
        except Exception as e:
            raise NetworkSecurityException(e)
    
    def predict(self, scaled_x):
        try:
            logging.info("PROCEDURE: Model Prediction, STATUS[3 of 3]: Complete.")
            return self.model.predict(scaled_x)
        
        except Exception as e:
            raise NetworkSecurityException(e)

