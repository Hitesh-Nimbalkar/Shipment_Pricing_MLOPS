
from shipment_pricing.entity.config_entity import SavedModelConfig
from shipment_pricing.utils.main_utils import read_yaml_file,load_numpy_array_data,save_object,check_folder_contents,load_object
from sklearn.ensemble import RandomForestRegressor
from shipment_pricing.entity.artifact_entity import DataTransformationArtifact,ParamOptimzeArtifact
from shipment_pricing.exception.exception import ApplicationException
from shipment_pricing.logger.logging import logging
from shipment_pricing.entity.config_entity import SavedModelConfig
from shipment_pricing.constant import *
from sklearn.metrics import r2_score
import yaml
import sys 


class ParamOptimize:
    def __init__(self,data_transformation_artifact:DataTransformationArtifact) -> None:
        
        
        self.data_transformation_artifact=data_transformation_artifact
        
        
        # Accessing Saved model to paramterize 
        self.saved_model_config = SavedModelConfig()
        self.Saved_model=self.saved_model_config.saved_model_object_path
        self.Saved_model_report=self.saved_model_config.saved_model_report_path
        
    def create_model_report(self,experiment,run_name,best_params, r2, model_label):
        # Creating a dictionary to store the model report information
        model_report = {
            'Experiment': experiment,
            'Run_name': run_name,
            'R2_score': str(r2),
            'parameters': best_params,
            'Model_name': model_label
        }
        
        return model_report
    
    def save_model_and_report(self,best_model, model_report, model_file_path,report_file_path):
        # Saving Model Report and Model object
        save_object(file_path=model_file_path, obj=best_model)

        # Save the report as a YAML file
        with open(report_file_path, 'w') as file:
            yaml.dump(model_report, file)
        logging.info("Model and report saved to Artifact Folder.")
        

        # Save the report as a params.yaml
        file_path = os.path.join('params.yaml')
        with open(file_path, 'w') as file:
            yaml.dump(model_report, file)
        logging.info("Params.yaml file saved to the directory.")

    
    
    def optimizing_params(self):
        try:
        
            y_test=load_numpy_array_data(file_path=self.data_transformation_artifact.test_target_file_path).ravel()
                
            X_test=load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_test_file_path)

            
            logging.info(f"Training Model of paramaters from params.yaml .............")
            
            saved_model=load_object(file_path=self.Saved_model)
            saved_model_report=read_yaml_file(file_path=self.Saved_model_report)

            # Extract parameters
            max_depth = int(saved_model_report['parameters']['max_depth'])
            min_samples_split = int(saved_model_report['parameters']['min_samples_split'])
            n_estimators = int(saved_model_report['parameters']['n_estimators'])

            # passing params to the saved modeol
            if isinstance(saved_model, RandomForestRegressor):
                # Set the parameters in the saved model
                saved_model.set_params(max_depth=max_depth, min_samples_split=min_samples_split, n_estimators=n_estimators)

                predictions = saved_model.predict(X_test)
                r2 = r2_score(y_test, predictions)
                logging.info(f'R2 Score of updated parameters : {r2}')
                
                saved_model_score=float(saved_model_report['R2_score'])
                
                if r2 > saved_model_score:
                    # Extracting information from the saved model report
                    experiment = saved_model_report['Experiment']
                    Model_name = saved_model_report['Model_name']
                    R2_score = r2
                    Run_name = saved_model_report['Run_name']
                    
                    # Parameters used in the current training
                    parameters = {
                        'max_depth': max_depth,
                        'min_samples_split': min_samples_split,
                        'n_estimators': n_estimators
                    }
                    
                    # Creating a new model report
                    model_report = self.create_model_report(
                        experiment=experiment,
                        run_name=Run_name,
                        best_params=parameters,
                        model_label=Model_name,
                        r2=R2_score
                    )
                    
                    # Saving the new model object and model report
                    self.save_model_and_report(
                        best_model=saved_model,
                        model_report=model_report,
                        model_file_path=self.model_training_config.model_object_file_path,
                        report_file_path=self.model_training_config.model_report
                    )
                    
                    # Logging information for successful model training
                    logging.info("Model trained is selected and saved to the directory")
                else:
                    # Logging information if the saved model has a higher score than the trained model
                    logging.info("Saved model has a higher score than the trained model")
                                
            param_optimise_artifact=ParamOptimzeArtifact(model_report=self.Saved_model_report,
                                                                            model_file_path=self.Saved_model)

            return param_optimise_artifact
        except Exception as e:
            raise ApplicationException(e, sys)
                
                
            
                
                
            
                
        
                