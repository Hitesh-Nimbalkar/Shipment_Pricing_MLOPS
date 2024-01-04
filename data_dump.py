import pandas as pd
import json
import os
from src.shipment_pricing.data_access.mongo_access import mongo_client
from data_schema import write_schema_yaml
from src.shipment_pricing.utils.main_utils import read_yaml_file

def get_project_config():
    config_file_path = os.path.join(os.getcwd(), 'config', 'config.yaml')
    return read_yaml_file(config_file_path)

def get_data_file_path(data_file_label):
    return os.path.join(os.getcwd(), 'data', data_file_label)

def get_mongo_client():
    return mongo_client()

def ingest_data_to_mongo(client, database_name, collection_name, data_file_path):
    write_schema_yaml(csv_file=data_file_path)
    
    df = pd.read_csv(data_file_path)
    print(f"Rows and columns: {df.shape}")

    df.reset_index(drop=True, inplace=True)

    json_record = list(json.loads(df.T.to_json()).values())
    print(json_record[0])

    client[database_name][collection_name].insert_many(json_record)

if __name__ == "__main__":
    project_config = get_project_config()
    data_file_label = project_config['data_file_label']
    data_ingestion_config = project_config['data_ingestion_config']
    data_base = data_ingestion_config['data_base']
    collection_name = data_ingestion_config['collection_name']

    data_file_path = get_data_file_path(data_file_label)
    client = get_mongo_client()

    ingest_data_to_mongo(client, data_base, collection_name, data_file_path)
