import pandas as pd
import logging
from src.shipment_pricing.exception.exception import ApplicationException
from src.shipment_pricing.data_access.mongo_access import mongo_client
import sys

def get_collection_as_dataframe(database_name: str, collection_name: str) -> pd.DataFrame:
    if not database_name or not collection_name:
        raise ValueError("Database name and collection name cannot be empty.")

    try:
        with mongo_client() as client:
            logging.info(f"Reading data from database: {database_name} and collection: {collection_name}")
            df = pd.DataFrame(list(client[database_name][collection_name].find()))

            if "_id" in df.columns:
                logging.info(f"Dropping column: _id ")
                df = df.drop("_id", axis=1)

            logging.info(f"Rows and columns in df: {df.shape}")
            return df

    except ValueError as ve:
        raise ApplicationException(ve, sys.exc_info())
    except Exception as e:
        raise ApplicationException(e, sys.exc_info())