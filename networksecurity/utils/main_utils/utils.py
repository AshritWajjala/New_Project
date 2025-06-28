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