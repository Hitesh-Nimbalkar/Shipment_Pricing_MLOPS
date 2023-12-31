
import pandas as pd
import json
import os
from src.shipment_pricing.data_access.mongo_access import mongo_client
from data_schema import write_schema_yaml
from src.shipment_pricing.utils.main_utils import read_yaml_file



# Extracting project config 
config_file_path=os.path.join(os.getcwd(),'config','config.yaml')
project_config=read_yaml_file(config_file_path)
# Accessing file Label 
data_file_lable=project_config['data_file_label']

# Data Ingestion config 
data_ingestion_config=project_config['data_ingestion_config']
data_base=data_ingestion_config['data_base']
collection_name=data_ingestion_config['collection_name']


# Accessing Mongo client for database access
client = mongo_client()
DATA_FILE_PATH =os.path.join(os.getcwd(),'data',data_file_lable)
DATABASE_NAME = data_base
COLLECTION_NAME = collection_name


if __name__=="__main__":
    
    write_schema_yaml(csv_file=DATA_FILE_PATH)
    
    df = pd.read_csv(DATA_FILE_PATH)
    print(f"Rows and columns: {df.shape}")

    df.reset_index(drop = True, inplace = True)

    json_record = list(json.loads(df.T.to_json()).values())
    print(json_record[0])

    client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_record)