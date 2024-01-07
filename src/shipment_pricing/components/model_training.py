from shipment_pricing.utils.main_utils import read_yaml_file,load_numpy_array_data,save_object,check_folder_contents,load_object
from sklearn.ensemble import RandomForestRegressor
from shipment_pricing.entity.config_entity import ModelTrainingConfig
from shipment_pricing.entity.artifact_entity import ModelTrainerArtifact,DataTransformationArtifact
from shipment_pricing.exception.exception import ApplicationException
from shipment_pricing.logger.logging import logging
from shipment_pricing.entity.config_entity import SavedModelConfig
from shipment_pricing.constant import *
import optuna
from sklearn.metrics import r2_score
import sys,yaml
import pandas as pd
import shutil
import numpy as np

class ModelOptimizer:
    def __init__(self, X_train, X_test, y_train, y_test, model_constructor, param_dict, n_trials=25):
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test
        self.best_params = None
        self.best_model = None
        self.r2 = None
        self.result_data = None
        self.model_constructor = model_constructor
        self.param_dict = param_dict
        self.n_trials = n_trials

    def objective(self, trial):
        param_dist = {
            'n_estimators': trial.suggest_categorical('n_estimators', self.param_dict['n_estimators']),
            'max_depth': trial.suggest_categorical('max_depth', self.param_dict['max_depth']),
            'min_samples_split': trial.suggest_categorical('min_samples_split', self.param_dict['min_samples_split']),
        }
        # Construct the model with sampled hyperparameters
        
        model = self.model_constructor(**param_dist)

        model.fit(self.X_train, self.y_train)
        y_pred = model.predict(self.X_test)
        r2 = r2_score(self.y_test, y_pred)
        

        return r2

    def optimize_model(self):
        study = optuna.create_study(direction='maximize')
        study.optimize(self.objective, n_trials=self.n_trials)

        self.best_params = study.best_params
        logging.info("Best Hyperparameters: %s", self.best_params)

        self.best_model = self.model_constructor(**self.best_params)
        self.best_model.fit(self.X_train, self.y_train)

        y_pred = self.best_model.predict(self.X_test)
        self.r2 = r2_score(self.y_test, y_pred)
        self.result_data = pd.DataFrame({'y_test': self.y_test, 'y_pred': y_pred})

        logging.info("R2 Score on Test Set: %s", self.r2)

        return self.best_params, self.r2, self.result_data, self.best_model

class model_training_config:
    def __init__(self, model_training_yaml, n_trials, X_train, X_test, y_train, y_test):
        self.model_training_yaml = model_training_yaml
        self.n_trials = n_trials
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test

    def optimize_and_log(self):
        # Accessing Model
        model_name =self.model_training_yaml['models']['name']
        # Access parameters
        parameters = self.model_training_yaml['models']['parameters']
        logging.info(f" Loading parameters for the model --- {model_name}")
        logging.info(f"Parameters ---  {parameters}")

        logging.info("Optimizing Model using Optuna... ")
        logging.info(f" Number of trials : {self.n_trials}")
        optimizer = ModelOptimizer(self.X_train, self.X_test, self.y_train, self.y_test, RandomForestRegressor, parameters, n_trials=self.n_trials)

        # Optimize the model
        best_params, r2, result_data, best_model = optimizer.optimize_model()
        # Log the optimization results
        logging.info("Optimization results:")
        logging.info(f"Best Parameters: {best_params}")
        logging.info(f"R-squared: {r2}")
        logging.info("Result Data: %s", result_data)
        logging.info("Best Model: %s", best_model)

        # Return relevant information
        return best_params, r2, best_model,model_name



class ModelTrainer :

    def __init__(self,model_training_config:ModelTrainingConfig,
                    data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_training_config=model_training_config
            self.data_transformation_artifact=data_transformation_artifact
            
            # Accessing config file paths 
            self.trained_model_path=self.model_training_config.model_object_file_path
            self.trained_model_report=self.model_training_config.model_report
            
            self.saved_model_config=SavedModelConfig()
            self.saved_model_dir=self.saved_model_config.saved_model_dir
            os.makedirs(self.saved_model_dir, exist_ok=True)
            self.saved_model_config_key=self.saved_model_config.saved_model_config_key
            
            
            # Loading yaml Dtaa from model Training.yaml
            self.model_training_yaml=read_yaml_file(file_path=MODEL_TRAINING_CONFIG_PATH)
            
            self.n_trials=self.model_training_yaml['optuna']['trials']
            logging.info(f" Number of Trials - {self.n_trials}")

            # Making model Training Directory in Artifact Folder
            self.model_train_artifact_dir=self.model_training_config.model_training_dir
            # Create the directory if it doesn't exist
            os.makedirs(self.model_train_artifact_dir, exist_ok=True)
            
            # Project Config Data 
            self.config_data = read_yaml_file(CONFIG_FILE_PATH)
            self.experiment=self.config_data[MODEL_TRAINING_CONFIG_KEY][MODEL_TRAINING_MLFLOW][MLFLOW_EXPERIMENT]
            self.run_id=self.config_data[MODEL_TRAINING_CONFIG_KEY][MODEL_TRAINING_MLFLOW][MLFLOW_RUN_ID]
            
            
        except Exception as e:
            raise ApplicationException(e, sys)
        
    
    def create_model_report(self,experiment,run_id,best_params, r2, model_label):
        # Creating a dictionary to store the model report information
        model_report = {
            'Experiment': experiment,
            'Run_id': run_id,
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

    
    
    def start_model_training(self):
        
        try:
            
            y_train=load_numpy_array_data(file_path=self.data_transformation_artifact.train_target_file_path).ravel()
            y_test=load_numpy_array_data(file_path=self.data_transformation_artifact.test_target_file_path).ravel()
            
            X_train=load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_train_file_path)
            X_test=load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_test_file_path)

            
            logging.info(f"Training target file path: {self.data_transformation_artifact.train_target_file_path}")
            logging.info(f"Test target file path: {self.data_transformation_artifact.test_target_file_path}")
            logging.info(f"Transformed training file path: {self.data_transformation_artifact.transformed_train_file_path}")
            logging.info(f"Transformed test file path: {self.data_transformation_artifact.transformed_test_file_path}")

            
            logging.info(f"Shape of the Transformed Data X_train: {X_train.shape} y_train: {y_train.shape}  X_test: {X_test.shape}  y_test: {y_test.shape}")
            
            # Check if params.yaml exists in the folder
            params_file_path = os.path.join(os.getcwd(), 'params.yaml')
            saved_model_directory=check_folder_contents(folder_path=self.saved_model_dir)
            
            
            if not os.path.exists(params_file_path) or not saved_model_directory:
                
                model_training_instance = model_training_config(self.model_training_yaml, self.n_trials, X_train, X_test, y_train, y_test)
                best_params, r2, best_model,model_label = model_training_instance.optimize_and_log()
                
                # Model Report
                model_report=self.create_model_report(self.experiment,
                                                      self.run_id,
                                                      best_params, 
                                                      r2, 
                                                      model_label
                                                      )
                # Saving Model Object and Model Report 
                self.save_model_and_report(best_model=best_model,
                                           model_report=model_report,
                                           model_file_path=self.model_training_config.model_object_file_path,
                                           report_file_path=self.model_training_config.model_report)
                
                # Copying Model and Report to saved model directory 
                # Copying Model 
                artifact_model_path=self.model_training_config.model_object_file_path
                saved_directory_model=self.saved_model_config.saved_model_object_path
                shutil.copy(artifact_model_path, saved_directory_model)
                # Copying Report 
                artifact_model_report_path=self.model_training_config.model_report
                saved_directory_model_report=self.saved_model_config.saved_model_report_path
                shutil.copy(artifact_model_report_path, saved_directory_model_report)
                
                
            else :
                
                logging.info(f"Training Model of paramaters from params.yaml .............")
                
                saved_model=load_object(file_path=self.saved_model_config.saved_model_object_path)
                saved_model_report=read_yaml_file(file_path=self.saved_model_config.saved_model_report_path)

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
                    
                    experiment=saved_model_report['Experiment']
                    Model_name=saved_model_report['Model_name']
                    R2_score=r2
                    Run_id=saved_model_report['Run_id']
                    parameters = {
                                        'max_depth': max_depth,
                                        'min_samples_split': min_samples_split,
                                        'n_estimators': n_estimators
                                }
                                    
                    model_report=self.create_model_report(experiment=experiment,
                                             run_id=Run_id,
                                             best_params=parameters,
                                             model_label=Model_name,
                                             r2=R2_score)
                    
                    # Saving Model Object and Model Report 
                    self.save_model_and_report(best_model=saved_model,
                                           model_report=model_report,
                                           model_file_path=self.model_training_config.model_object_file_path,
                                           report_file_path=self.model_training_config.model_report)
                    
                    logging.info(" Model Saved in Artifact folder ")
                    
                    

            model_trainer_artifact=ModelTrainerArtifact(trained_model_file_path=self.model_training_config.model_object_file_path,
                                                                            model_artifact_report=self.model_training_config.model_report)
                
                
                
            return model_trainer_artifact
        except Exception as e:
            raise ApplicationException(e, sys)
                
                
            
                