
import uuid
from src.shipment_pricing.entity.config_entity import *
from src.shipment_pricing.exception import ApplicationException
from src.shipment_pricing.utils.main_utils import read_yaml_file,write_yaml_file,add_dict_to_yaml
from src.shipment_pricing.entity.config_entity import *
from src.shipment_pricing.entity.artifact_entity import *
from src.shipment_pricing.components.data_validation import DataValidation
import  sys
from collections import namedtuple




class data_validation():

    def __init__(self,training_pipeline_config=TrainingPipelineConfig()) -> None:
        try:
            
            self.training_pipeline_config=training_pipeline_config
            artifact=read_yaml_file(ARTIFACT_ENTITY_YAML_FILE_PATH)
            data_ingestion_artifact=artifact['data_ingestion_artifact']
            train_path=data_ingestion_artifact['train_file_path']
            test_path=data_ingestion_artifact['test_file_path']
            
            
            data_validation = DataValidation(
                data_validation_config = DataValidationConfig(self.training_pipeline_config),
                data_ingestion_artifact = DataIngestionArtifact(train_file_path=train_path,
                                                                  test_file_path=test_path))

            data_validation_artifact=data_validation.initiate_data_validation()
            
            
            add_dict_to_yaml(file_path=ARTIFACT_ENTITY_YAML_FILE_PATH,new_data=data_validation_artifact)

        except Exception as e:
            raise ApplicationException(e, sys) from e
        
        
if __name__ == '__main__':
    data_transformation()