
from shipment_pricing.entity.config_entity import *
from shipment_pricing.entity.artifact_entity import *



class Model_pusher:
    def __init__(self,model_evaluation_artifact:ModelEvaluationArtifact) -> None:
        
        self.model_evaluation_artifact=model_evaluation_artifact
        
        self.model_path=self.model_evaluation_artifact.model_file_path
        self.model_report=self.model_evaluation_artifact.model_report
        
        
    def start_model_pusher(self):
        
        model_path=self.saved_model_path
        
        
        