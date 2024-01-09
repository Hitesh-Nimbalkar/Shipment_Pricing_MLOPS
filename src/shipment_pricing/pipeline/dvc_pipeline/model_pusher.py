import uuid
from shipment_pricing.entity.config_entity import *
from shipment_pricing.exception.exception import ApplicationException
from shipment_pricing.utils.main_utils import read_yaml_file,add_dict_to_yaml_dvc
from shipment_pricing.entity.config_entity import *
from shipment_pricing.entity.artifact_entity import *
import  sys
from shipment_pricing.components.model_pusher import Model_pusher



class model_evaluation():

    def __init__(self,training_pipeline_config=TrainingPipelineConfig()) -> None:
        try:
            
            self.training_pipeline_config=training_pipeline_config
            
            artifact=read_yaml_file(ARTIFACT_ENTITY_YAML_FILE_PATH)
            model_evaluation_artifact=artifact['model_evaluation']
            
            # Target Data 
            model_file_path=model_evaluation_artifact['model_file_path']
            report_file_path=model_evaluation_artifact['model_report']
            message=model_evaluation_artifact['message']
            
            model_pusher = Model_pusher(
                model_evaluation_artifact=ModelEvaluationArtifact(message=message,
                                                                model_file_path=model_file_path,
                                                                                          model_report=report_file_path))   
            model_pusher_artifact=model_pusher.start_model_pusher()
            
            add_dict_to_yaml_dvc(file_path=ARTIFACT_ENTITY_YAML_FILE_PATH ,new_data=model_pusher_artifact,label='model_pusher')
            
        except Exception as e:
            raise ApplicationException(e,sys) from e  
        
if __name__ == '__main__':
    model_evaluation()