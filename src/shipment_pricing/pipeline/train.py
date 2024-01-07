
from shipment_pricing.constant import *
from shipment_pricing.exception.exception import ApplicationException
from shipment_pricing.entity.config_entity import *
from shipment_pricing.entity.artifact_entity import *
from shipment_pricing.components.data_ingestion import DataIngestion
from shipment_pricing.components.data_validation import DataValidation
from shipment_pricing.components.data_transformation import DataTransformation
from shipment_pricing.components.model_training import ModelTrainer
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

    def start_data_transformation(self,data_validation_artifact: DataValidationArtifact) -> DataTransformationArtifact:
        try:
            data_transformation = DataTransformation(
                data_transformation_config = DataTransformationConfig(self.training_pipeline_config),
                data_validation_artifact = data_validation_artifact)

            return data_transformation.initiate_data_transformation()
        except Exception as e:
            raise ApplicationException(e,sys) from e
        
        
    def start_model_training(self,data_transformation_artifact: DataTransformationArtifact) -> ModelTrainerArtifact:
        try:
            model_trainer = ModelTrainer(model_training_config=ModelTrainingConfig(self.training_pipeline_config),
                                        data_transformation_artifact=data_transformation_artifact)   
            
            logging.info("Model Trainer intiated")

            return model_trainer.start_model_training()
        except Exception as e:
            raise ApplicationException(e,sys) from e  


    def run_pipeline(self):
            try:
                #data ingestion
                data_ingestion_artifact = self.start_data_ingestion()
                
                # data Validation 
                data_validation_artifact=self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
                
                # data transformation 
                data_transformation_artifact = self.start_data_transformation(data_validation_artifact=data_validation_artifact)
                
                # Model Trainer 
                model_trainer_artifact = self.start_model_training(data_transformation_artifact=data_transformation_artifact)
            
            except Exception as e:
                raise ApplicationException(e, sys) from e
            
