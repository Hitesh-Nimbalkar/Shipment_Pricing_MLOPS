
from shipment_pricing.entity.config_entity import SavedModelConfig,Param_Optimize_Config
from shipment_pricing.utils.main_utils import read_yaml_file,load_numpy_array_data,save_object,load_object
from sklearn.ensemble import RandomForestRegressor
from shipment_pricing.entity.artifact_entity import DataTransformationArtifact,ParamOptimzeArtifact,ModelTrainerArtifact
from shipment_pricing.exception.exception import ApplicationException
from shipment_pricing.logger.logging import logging
from shipment_pricing.entity.config_entity import SavedModelConfig
from shipment_pricing.constant import *
from sklearn.metrics import r2_score
import yaml
import sys 


class ParamOptimize:
    def __init__(self,data_transformation_artifact:DataTransformationArtifact,param_optimize_config:Param_Optimize_Config,
                 model_training_artifact:ModelTrainerArtifact) -> None:
        
        
        self.data_transformation_artifact=data_transformation_artifact
        self.param_optimize_config=param_optimize_config
        self.model_training_artifact=model_training_artifact
        
        # Artifact trained Model 
        self.artifact_model=self.model_training_artifact.model_file_path
        self.artifact_report=self.model_training_artifact.model_report
    
        # Newly trained Model 
        self.param_model=self.param_optimize_config.model_object_path
        self.param_report=self.param_optimize_config.model_report_path
        
        saved_model_config=SavedModelConfig()
        self.saved_model_directory=saved_model_config.saved_model_dir
        self.saved_model_object=saved_model_config.saved_model_object_path
        self.saved_model_report=saved_model_config.saved_model_report_path
        
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

    def train_model_with_params(self,X_test,y_test):
        
        logging.info("Training Model of parameters from params.yaml ........................")

        saved_model = load_object(file_path=self.saved_model_object)
        saved_model_report = read_yaml_file(file_path=self.saved_model_report)
        
        params_data=read_yaml_file('params.yaml')

        # Extract parameters
        max_depth = int(params_data['parameters']['max_depth'])
        min_samples_split = int(params_data['parameters']['min_samples_split'])
        n_estimators = int(params_data['parameters']['n_estimators'])
        
        # Log the parameters
        logging.info("---------------New Paramters--------------")
        logging.info(f"Max Depth: {max_depth}")
        logging.info(f"Min Samples Split: {min_samples_split}")
        logging.info(f"N Estimators: {n_estimators}")

        # passing params to the saved model
        if isinstance(saved_model, RandomForestRegressor):
            # Set the parameters in the saved model
            saved_model.set_params(max_depth=max_depth, 
                                   min_samples_split=min_samples_split, 
                                   n_estimators=n_estimators)

            predictions = saved_model.predict(X_test)
            r2 = r2_score(y_test, predictions)
            logging.info(f'R2 Score of updated parameters: {r2}')
            

            # Extracting information from params 
            experiment = params_data['Experiment']
            Model_name = params_data['Model_name']
            R2_score = r2
            Run_name = params_data['Run_name']

                # Parameters used in the current training
            parameters = {
                    'max_depth': max_depth,
                    'min_samples_split': min_samples_split,
                    'n_estimators': n_estimators
                }
            
            logging.info(" creating new report ")

            # Creating a new model report
            model_report = self.create_model_report(
                experiment=experiment,
                run_name=Run_name,
                best_params=parameters,
                model_label=Model_name,
                r2=R2_score
            )
            logging.info(" Saving new report and Model in Artifact Directory  ")

            # Saving the new model object and model report
            self.save_model_and_report(
                best_model=saved_model,
                model_report=model_report,
                model_file_path=self.param_model,
                report_file_path=self.param_report
            )
            
            logging.info("Saving Model with latest parametrs passed from params.yaml")


                
                

    
    def optimizing_params(self):
        try:
        
            y_test=load_numpy_array_data(file_path=self.data_transformation_artifact.test_target_file_path).ravel()
                
            X_test=load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_test_file_path)
            
            
            if os.path.exists('params.yaml') and os.path.exists(self.saved_model_directory) and os.listdir(self.saved_model_directory):

                
                logging.info(f"Training Model of paramaters from params.yaml .............")
                
                self.train_model_with_params(X_test=X_test,y_test=y_test)
                
                
                
            else:
            
                artifact_model=load_object(file_path=self.artifact_model)
                artifact_model_report=read_yaml_file(file_path=self.artifact_report)
        
                self.save_model_and_report(
                    best_model=artifact_model,
                    model_report=artifact_model_report,
                    model_file_path=self.param_model,
                    report_file_path=self.param_report
                )
                
                
        

                                
            param_optimise_artifact=ParamOptimzeArtifact(model_report=self.param_report,
                                                                            model_file_path=self.param_model)

            return param_optimise_artifact
        except Exception as e:
            raise ApplicationException(e, sys)
                
                
            
                
                
            
                
        
                