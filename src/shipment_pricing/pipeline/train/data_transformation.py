
import uuid
from shipment_pricing.entity.config_entity import *
from shipment_pricing.exception import ApplicationException
from shipment_pricing.utils.main_utils import read_yaml_file,write_yaml_file,add_dict_to_yaml
from shipment_pricing.entity.config_entity import *
from shipment_pricing.entity.artifact_entity import *
from shipment_pricing.components.data_transformation import DataTransformation
import  sys
from collections import namedtuple




class data_transformation():

    def __init__(self,training_pipeline_config=TrainingPipelineConfig()) -> None:
        try:
            
            self.training_pipeline_config=training_pipeline_config
            artifact=read_yaml_file(ARTIFACT_ENTITY_YAML_FILE_PATH)
            data_ingestion_artifact=artifact['data_ingestion_artifact']
            train_path=data_ingestion_artifact['train_file_path']
            test_path=data_ingestion_artifact['test_file_path']
            
            
            data_transformation = DataTransformation(
                data_transformation_config = DataTransformationConfig(self.training_pipeline_config),
                data_ingestion_artifact = DataIngestionArtifact(train_file_path=train_path,
                                                                  test_file_path=test_path))
            
            

            data_transformation_artifact=data_transformation.initiate_data_transformation()
                                                                          
            
            add_dict_to_yaml(file_path=ARTIFACT_ENTITY_YAML_FILE_PATH,new_data=data_transformation_artifact)

        except Exception as e:
            raise ApplicationException(e, sys) from e
        
        
if __name__ == '__main__':
    data_transformation()