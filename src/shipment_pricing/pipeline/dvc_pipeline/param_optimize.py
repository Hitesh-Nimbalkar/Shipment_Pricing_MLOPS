import uuid
from shipment_pricing.entity.config_entity import *
from shipment_pricing.exception.exception import ApplicationException
from shipment_pricing.utils.main_utils import read_yaml_file,add_dict_to_yaml_dvc
from shipment_pricing.entity.artifact_entity import *
import  sys
from shipment_pricing.components.param_optimize import ParamOptimize




class param_optimizer():

    def __init__(self,training_pipeline_config=TrainingPipelineConfig()) -> None:
        try:
            
            self.training_pipeline_config=training_pipeline_config
            
            artifact=read_yaml_file(ARTIFACT_ENTITY_YAML_FILE_PATH)
            data_transformation_artifact=artifact['data_transformation']
            
            # Target Data 
            target_test=data_transformation_artifact['test_target_file_path']
            target_train=data_transformation_artifact['train_target_file_path']
            transform_object_path=data_transformation_artifact['feature_engineering_object_file_path']
            transformed_test_path=data_transformation_artifact['transformed_test_file_path']
            transformed_train_path=data_transformation_artifact['transformed_train_file_path']
            
            
            param_optimize = ParamOptimize( data_transformation_artifact=DataTransformationArtifact(feature_engineering_object_file_path=transform_object_path,
                                                                                                transformed_train_file_path=transformed_train_path,
                                                                                                test_target_file_path=target_test,
                                                                                                train_target_file_path=target_train,
                                                                                                transformed_test_file_path=transformed_test_path))   
            param_optimize_artifact=param_optimize.optimizing_params()
            
            add_dict_to_yaml_dvc(file_path=ARTIFACT_ENTITY_YAML_FILE_PATH ,new_data=param_optimize_artifact,label='param_optimizer')
            
        except Exception as e:
            raise ApplicationException(e,sys) from e  
        
if __name__ == '__main__':
    param_optimizer()