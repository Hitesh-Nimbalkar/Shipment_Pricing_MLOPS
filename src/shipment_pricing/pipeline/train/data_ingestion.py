

from src.shipment_pricing.exception.exception import ApplicationException
from typing import List
from src.shipment_pricing.utils.main_utils import read_yaml_file
from multiprocessing import Process
from src.shipment_pricing.entity.config_entity import *
from src.shipment_pricing.entity.artifact_entity import *
from src.shipment_pricing.components.data_ingestion import DataIngestion
import  sys





class data_ingestion():

    def __init__(self,training_pipeline_config=TrainingPipelineConfig()) -> None:
        try:
            
            self.training_pipeline_config=training_pipeline_config
            data_ingestion = DataIngestion(data_ingestion_config=DataIngestionConfig(self.training_pipeline_config))
            data_ingestion.initiate_data_ingestion()
            
        except Exception as e:
            raise ApplicationException(e, sys) from e

        
if __name__ == '__main__':
    data_ingestion()