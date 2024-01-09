
from shipment_pricing.entity.config_entity import *
from shipment_pricing.entity.artifact_entity import *
import shutil


class Model_pusher:
    def __init__(self,model_evaluation_artifact:ModelEvaluationArtifact) -> None:
        
        self.model_evaluation_artifact=model_evaluation_artifact
        
        self.model_path=self.model_evaluation_artifact.model_file_path
        self.model_report=self.model_evaluation_artifact.model_report
        
        
        saved_model_config=SavedModelConfig()
        self.saved_model_object=saved_model_config.saved_model_object_path
        self.saved_model_report=saved_model_config.saved_model_report_path
        
        
    def start_model_pusher(self):
        
        
        # Copying contents to saved Directory
           
        # Copying Model 
        shutil.copy(self.model_path, self.saved_model_object)
        # Copying Report 
        shutil.copy(self.model_report, self.saved_model_report)
        
        shutil.copy(self.model_report, 'params.yaml')
        
        
        model_pusher_artifact= ModelPusherArtifact(message="training pipeine Complete")
       
        return model_pusher_artifact
        
        
        



        
        