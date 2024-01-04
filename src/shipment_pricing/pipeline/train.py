
from src.shipment_pricing.constant import *
from src.shipment_pricing.exception.exception import ApplicationException
from src.shipment_pricing.entity.config_entity import *
from src.shipment_pricing.entity.artifact_entity import *
from src.shipment_pricing.components.data_ingestion import DataIngestion
from src.shipment_pricing.components.data_validation import DataValidation
import  sys



class Pipeline():

    def __init__(self,training_pipeline_config=TrainingPipelineConfig()):
        try:
            
            self.training_pipeline_config=training_pipeline_config
            
        except Exception as e:
            raise ApplicationException(e, sys) from e

    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            data_ingestion = DataIngestion(data_ingestion_config=DataIngestionConfig(self.training_pipeline_config))
            return data_ingestion.initiate_data_ingestion()
        except Exception as e:
            raise ApplicationException(e, sys) from e
        
    def start_data_validation(self, data_ingestion_artifact:DataIngestionArtifact)-> DataValidationArtifact:
        try:
            data_validation = DataValidation(data_validation_config=DataValidationConfig(self.training_pipeline_config),
                                             data_ingestion_artifact=data_ingestion_artifact)
            return data_validation.initiate_data_validation()
        except Exception as e:
            raise ApplicationException(e, sys) from e
        


    def run_pipeline(self):
            try:
                #data ingestion
                data_ingestion_artifact = self.start_data_ingestion()
                
                # data Validation 
                data_validation_artifact=self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            
            except Exception as e:
                raise ApplicationException(e, sys) from e
            
