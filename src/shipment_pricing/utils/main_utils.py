import yaml
from src.shipment_pricing.exception.exception import ApplicationException
import os,sys


def write_yaml_file(file_path:str, data:dict = None):
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
    
    
def add_dict_to_yaml(file_path, new_data):
    try:
        # Load the existing YAML data
        with open(file_path, 'r') as file:
            existing_data = yaml.safe_load(file)

        # Merge the existing data with the new dictionary data
        existing_data.update(new_data)

        # Write the updated data back to the file
        with open(file_path, 'w') as file:
            yaml.dump(existing_data, file, default_flow_style=False)

        print("Data added successfully.")
    except Exception as e:
        print("An error occurred:", e)