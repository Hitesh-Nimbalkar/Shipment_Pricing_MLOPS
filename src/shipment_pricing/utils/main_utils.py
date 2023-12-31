import yaml
from src.shipment_pricing.exception.exception import ApplicationException
import os,sys
import dill
import pandas as pd
import numpy as np


def write_ymal_file(file_path:str, data:dict = None):
    try:
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path, 'w') as f:
            if data is not None:
                yaml.dump_all(data, f)
    except Exception as e:
        raise ApplicationException(e,sys) from e

def read_yaml_file(file_path:str)->dict:
    """
    Reads a YAML file and returns the contents as dictionary.
    Params:
    ---------------
    file_path (str) : file path for the yaml file
    """
    try:
        with open(file_path,"rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise ApplicationException(e,sys) from e