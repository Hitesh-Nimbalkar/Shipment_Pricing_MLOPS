
from shipment_pricing.entity.config_entity import *
from shipment_pricing.exception.exception import ApplicationException
from shipment_pricing.utils.main_utils import read_yaml_file,add_dict_to_yaml_dvc
from shipment_pricing.entity.config_entity import *
from shipment_pricing.entity.artifact_entity import *
from shipment_pricing.components.data_transformation import DataTransformation
from shipment_pricing.components.data_validation import DataValidation
import  sys




class data_transformation():

    def __init__(self,training_pipeline_config=TrainingPipelineConfig()) -> None:
        try:
            
            self.training_pipeline_config=training_pipeline_config
            artifact=read_yaml_file(ARTIFACT_ENTITY_YAML_FILE_PATH)
            data_validation=artifact['data_validation']
            validated_train_path=data_validation['validated_train_path']
            validated_test_path=data_validation['validated_test_path']
            
            
            data_transformation = DataTransformation(
                data_transformation_config = DataTransformationConfig(self.training_pipeline_config),
                data_validation_artifact = DataValidationArtifact(validated_train_path=validated_train_path,
                                                                  validated_test_path=validated_test_path))
            
            

            data_transformation_artifact=data_transformation.initiate_data_transformation()
                                                                          
            
            add_dict_to_yaml_dvc(file_path=ARTIFACT_ENTITY_YAML_FILE_PATH ,new_data=data_transformation_artifact,label='data_transformation')

        except Exception as e:
            raise ApplicationException(e, sys) from e
        
        
if __name__ == '__main__':
    data_transformation()