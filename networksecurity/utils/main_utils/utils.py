import yaml
import os
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
import numpy as np
import dill
import pickle

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
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as f:
            np.save(f, array)

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
    