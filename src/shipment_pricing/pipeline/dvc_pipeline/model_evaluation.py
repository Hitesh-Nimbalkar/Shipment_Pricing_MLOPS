import uuid
from shipment_pricing.entity.config_entity import *
from shipment_pricing.exception.exception import ApplicationException
from shipment_pricing.utils.main_utils import read_yaml_file,add_dict_to_yaml_dvc
from shipment_pricing.entity.config_entity import *
from shipment_pricing.entity.artifact_entity import *
import  sys
from shipment_pricing.components.model_evaluation import ModelEvaluation



class model_evaluation():

    def __init__(self,training_pipeline_config=TrainingPipelineConfig()) -> None:
        try:
            
            self.training_pipeline_config=training_pipeline_config
            
            artifact=read_yaml_file(ARTIFACT_ENTITY_YAML_FILE_PATH)
            param_optimize_artifact=artifact['param_optimizer']
            
            # Target Data 
            model_file_path=param_optimize_artifact['model_file_path']
            report_file_path=param_optimize_artifact['model_report']

            
            model_evaluation = ModelEvaluation(model_evaluation_config=ModelEvalConfig,
                param_optimize_artifact=ParamOptimzeArtifact(model_file_path=model_file_path,
                                                                                          model_report=report_file_path))   
            model_evaluation_artifact=model_evaluation.initiate_model_evaluation()
            
            add_dict_to_yaml_dvc(file_path=ARTIFACT_ENTITY_YAML_FILE_PATH ,new_data=model_evaluation_artifact,label='model_evaluation')
            
        except Exception as e:
            raise ApplicationException(e,sys) from e  
        
if __name__ == '__main__':
    model_evaluation()