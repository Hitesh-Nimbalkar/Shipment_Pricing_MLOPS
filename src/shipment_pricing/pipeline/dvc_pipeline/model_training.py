
        
     
import uuid
from shipment_pricing.entity.config_entity import *
from shipment_pricing.exception.exception import ApplicationException
from typing import List
from shipment_pricing.utils.main_utils import read_yaml_file,add_dict_to_yaml_dvc
from multiprocessing import Process
from shipment_pricing.entity.config_entity import *
from shipment_pricing.entity.artifact_entity import *
from shipment_pricing.components.model_training import ModelTrainer

import  sys
from collections import namedtuple




class model_trainer():

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
            

            
            model_trainer = ModelTrainer(model_training_config=ModelTrainingConfig(self.training_pipeline_config),
                                        data_transformation_artifact=DataTransformationArtifact(feature_engineering_object_file_path=transform_object_path,
                                                                                                transformed_train_file_path=transformed_train_path,
                                                                                                test_target_file_path=target_test,
                                                                                                train_target_file_path=target_train,
                                                                                                transformed_test_file_path=transformed_test_path))   
            model_trainer_artifact=model_trainer.start_model_training()
            
            add_dict_to_yaml_dvc(file_path=ARTIFACT_ENTITY_YAML_FILE_PATH ,new_data=model_trainer_artifact,label='model_trainer')
            
        except Exception as e:
            raise ApplicationException(e,sys) from e  
        
if __name__ == '__main__':
    model_trainer()
        