from shipment_pricing.exception.exception import ApplicationException
from shipment_pricing.utils.main_utils import write_yaml_file_dvc
from shipment_pricing.entity.config_entity import *
from shipment_pricing.entity.artifact_entity import *
from shipment_pricing.components.data_ingestion import DataIngestion
import  sys



class data_ingestion():

    def __init__(self,training_pipeline_config=TrainingPipelineConfig()) -> None:
        try:
            
            self.training_pipeline_config=training_pipeline_config
            data_ingestion = DataIngestion(data_ingestion_config=DataIngestionConfig(self.training_pipeline_config))
            data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
            
            write_yaml_file_dvc(file_path=ARTIFACT_ENTITY_YAML_FILE_PATH ,obj=data_ingestion_artifact,label='data_ingestion')
            
            
        except Exception as e:
            raise ApplicationException(e, sys) from e

        
if __name__ == '__main__':

    file_path = 'params.yaml'

    # Check if the file exists
    if os.path.exists(file_path):
        # If it exists, delete it
        os.remove(file_path)
        print(f"The file {file_path} has been deleted.")
    else:
        print(f"The file {file_path} does not exist.")

    data_ingestion()