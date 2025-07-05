from networksecurity.entity.artifact_entity import ClassificationMetricArtifact
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from sklearn.metrics import f1_score, precision_score, recall_score

def get_classification_score(y_test, y_pred):
    """
    This method returns the metrics of the model.
    Input:
        y_true --> true target/dependent values(np.array)
        y_pred --> predicted target/dependent values(np.array)
    
    Output:
        F1 score, Precision score, Recall score.
    """
    try:

        model_f1_score = f1_score(y_test, y_pred) 
        model_precision_score = precision_score(y_test, y_pred)
        model_recall_score = recall_score(y_test, y_pred)

        return ClassificationMetricArtifact(
            f1_score=model_f1_score,
            precision_score=model_precision_score,
            recall_score=model_recall_score
        )
    
    except Exception as e:
        raise NetworkSecurityException