import os,sys
from shipment_pricing.exception.exception import ApplicationException
from shipment_pricing.logger.logging import logging
from shipment_pricing.utils.main_utils import read_yaml_file
from shipment_pricing.constant import *



config_data=read_yaml_file(CONFIG_FILE_PATH)

class TrainingPipelineConfig:
    
    def __init__(self):
        try:
            training_pipeline_config=config_data['training_pipeline_config']
            artifact_dir=training_pipeline_config['artifact']
            self.artifact_dir = os.path.join(os.getcwd(),artifact_dir)
        except Exception  as e:
            raise ApplicationException(e,sys)    


class DataIngestionConfig:
    
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            data_ingestion_key=config_data[DATA_INGESTION_CONFIG_KEY]
            
            self.database_name=data_ingestion_key[DATA_INGESTION_DATABASE_NAME]
            self.collection_name=data_ingestion_key[DATA_INGESTION_COLLECTION_NAME]
            
            self.data_ingestion_dir = os.path.join(training_pipeline_config.artifact_dir ,data_ingestion_key[DATA_INGESTION_ARTIFACT_DIR])
            self.raw_data_dir = os.path.join(self.data_ingestion_dir,data_ingestion_key[DATA_INGESTION_RAW_DATA_DIR_KEY])
            self.ingested_data_dir=os.path.join(self.raw_data_dir,data_ingestion_key[DATA_INGESTION_INGESTED_DIR_NAME_KEY])
            self.train_file_path = os.path.join(self.ingested_data_dir,data_ingestion_key[DATA_INGESTION_TRAIN_DIR_KEY])
            self.test_file_path = os.path.join(self.ingested_data_dir,data_ingestion_key[DATA_INGESTION_TEST_DIR_KEY])
            self.split_size = data_ingestion_key[SPLIT_SIZE]
            
            
        except Exception  as e:
            raise ApplicationException(e,sys)      


class DataValidationConfig:
    
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
        
            data_validation_key=config_data[DATA_VALIDATION_CONFIG_KEY]
            self.data_validation_dir = os.path.join(training_pipeline_config.artifact_dir ,data_validation_key[DATA_VALIDATION_ARTIFACT_DIR])
            self.validated_dir=os.path.join(training_pipeline_config.artifact_dir,data_validation_key[DATA_VALIDATION_VALID_DATASET])
            self.validated_train_path=os.path.join(self.data_validation_dir,data_validation_key[DATA_VALIDATION_TRAIN_FILE])
            self.validated_test_path=os.path.join(self.data_validation_dir,data_validation_key[DATA_VALIDATION_TEST_FILE])
            self.schema_file_path=SCHEMA_FILE_PATH
        
        except Exception  as e:
            raise ApplicationException(e,sys)      

class DataTransformationConfig:
    
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        
        
        data_transformation_key=config_data[DATA_TRANSFORMATION_CONFIG_KEY]
        
        self.data_transformation_dir = os.path.join(training_pipeline_config.artifact_dir , data_transformation_key[DATA_TRANSFORMATION])
        self.transformation_dir = os.path.join(self.data_transformation_dir,data_transformation_key[DATA_TRANSFORMATION_DIR_NAME_KEY])
        self.transformed_train_dir = os.path.join(self.transformation_dir,data_transformation_key[DATA_TRANSFORMATION_TRAIN_DIR_NAME_KEY])
        self.transformed_test_dir = os.path.join(self.transformation_dir,data_transformation_key[DATA_TRANSFORMATION_TEST_DIR_NAME_KEY])
        self.preprocessed_dir = os.path.join(self.data_transformation_dir,data_transformation_key[DATA_TRANSFORMATION_PREPROCESSING_DIR_KEY])
        self.feature_engineering_object_file_path =os.path.join(self.preprocessed_dir,data_transformation_key[DATA_TRANSFORMATION_FEA_ENG_FILE_NAME_KEY])
        self.preprocessor_file_object_file_path=os.path.join(self.preprocessed_dir,data_transformation_key[DATA_TRANSFORMATION_PREPROCESSOR_NAME_KEY])
        
        
        
class ModelTrainingConfig:
    
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        
        model_training_key=config_data[MODEL_TRAINING_CONFIG_KEY]

        self.model_training_dir = os.path.join(training_pipeline_config.artifact_dir ,model_training_key[MODEL_TRAINER_ARTIFACT_DIR])
        self.model_object_file_path = os.path.join(self.model_training_dir,model_training_key[MODEL_TRAINER_OBJECT])
        self.model_report =  os.path.join(self.model_training_dir,model_training_key[MODEL_REPORT_FILE])

class SavedModelConfig:
    
    def __init__(self):
        self.saved_model_config_key=config_data[SAVED_MODEL_CONFIG_KEY]
        ROOT_DIR=os.getcwd()
        self.saved_model_dir=os.path.join(ROOT_DIR,self.saved_model_config_key[SAVED_MODEL_DIR])
        self.saved_model_object_path=os.path.join(self.saved_model_dir,self.saved_model_config_key[SAVED_MODEL_OBJECT])
        self.saved_model_report_path=os.path.join(self.saved_model_dir,self.saved_model_config_key[SAVED_MODEL_REPORT])
        



class Param_Optimize_Config:
    
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        
        
        param_optimize_config_key=config_data[PARAM_OPTIMIZE_CONFIG_KEY]        
        
        self.param_optimize_directory=os.path.join(training_pipeline_config.artifact_dir ,param_optimize_config_key[PARAM_OPTIMIZE_DIRECTORY])
        self.model_object_path=os.path.join(self.param_optimize_directory,param_optimize_config_key[PARAM_OPTIMIZE_MODEL])
        self.model_report_path=os.path.join(self.param_optimize_directory,param_optimize_config_key[PARAM_OPTIMIZE_MODEL_REPORT])
        
        
         
        
class ModelEvalConfig:
    
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        
        
        model_eval_config_key=config_data[MODEL_EVAL_CONFIG_KEY]        
        
        self.model_eval_directory=os.path.join(training_pipeline_config.artifact_dir ,model_eval_config_key[MODEL_EVALUATION_DIRECTORY])
        self.model_eval_object=os.path.join(self.model_eval_directory,model_eval_config_key[MODEL_EVALUATION_OBJECT])
        self.model_eval_report=os.path.join(self.model_eval_directory,model_eval_config_key[MODEL_REPORT])
        
        
        