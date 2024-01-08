
from shipment_pricing.exception.exception import ApplicationException
from shipment_pricing.logger.logging import logging
import sys
from shipment_pricing.utils.main_utils import *
from shipment_pricing.entity.config_entity import *
from shipment_pricing.entity.artifact_entity import *
from shipment_pricing.constant import *
from shipment_pricing.utils.main_utils import read_yaml_file,load_object
from shipment_pricing.constant import *
from mlflow.tracking import MlflowClient
from mlflow.tracking.artifact_utils import _download_artifact_from_uri
import mlflow
from mlflow.sklearn import log_model
import joblib


class Experiments_evaluation:
    def __init__(self) :
        
        self.best_model_run_id=None
        self.best_model_uri=None
        self.artifact_uri = None
        

    def read_report(self,report_data,model):
        
        self.R2_score = report_data['R2_score']
        self.parameters=report_data['parameters']
        self.Model_name=report_data['Model_name']
        self.experiment_name=report_data['Experiment']
        self.run_name=report_data['Run_name']
        
        self.saved_model=model
        
            
    def get_best_model_run_id(self,experiment_name, metric_name):
        # Get the experiment ID
        experiment_id = mlflow.get_experiment_by_name(experiment_name).experiment_id
        
        # Retrieve runs and sort by the specified metric
        runs = mlflow.search_runs(experiment_ids=[experiment_id], filter_string='', order_by=[f"metrics.{metric_name} DESC"])
        
        if runs.empty:
            print("No runs found for the specified experiment and metric.")
            return None
        
        # Get the best run 
        best_run = runs.iloc[0]
        self.best_model_run_id = best_run.run_id
        
        # Load the best model
        self.best_model_uri=(f"runs:/{self.best_model_run_id}/{self.Model_name}")


    def download_model_and_generate_report(self, mlflow_server_uri="http://localhost:5000"):
        # Set the tracking URI to the local MLflow server
        mlflow.set_tracking_uri(mlflow_server_uri)

        # Load the run
        run = mlflow.get_run(self.best_model_run_id)

        if run is None:
            raise ValueError("Run not found with ID: {}".format(self.best_model_run_id))

        # Extract parameters and metrics
        parameters = run.data.params
        model_name = parameters.get("Model_name", "N/A")
        r2_score = run.data.metrics.get("R2_score", "N/A")

        # Manually log the run name as a parameter (modify as needed)
        run_name = parameters.get("Run_name", "N/A")

        # Load the model
        loaded_model = mlflow.pyfunc.load_model(self.best_model_uri)

        # Create a dictionary with the extracted information
        report_data = {
            "Experiment": self.experiment_name,
          #  "Experiment_id": run.info.experiment_id,
            "Run_name": run_name,
            "Model_name": model_name,
            "R2_score": r2_score,
          #  "Run_id": self.best_model_run_id,
            "parameters": parameters
        }

        return report_data, loaded_model


    def run_mlflow_experiment(self):
        
        # Create or get the experiment
        mlflow.set_experiment(self.experiment_name)
        
        # Start a run
        with mlflow.start_run(run_name=self.run_name):
            # Log metrics, params, and model
            mlflow.log_metric("R2_score", float(self.R2_score))
            mlflow.log_params(self.parameters)
            mlflow.set_tag("parameters", "custom_tag")
            mlflow.sklearn.log_model(self.saved_model,self.Model_name)
        
        logging.info("Checking for best model from the Mlflow Logs")
        
        self.get_best_model_run_id(metric_name='R2_score', experiment_name=self.experiment_name)
        
        print(f"Best model Run id: {self.best_model_run_id}")

        return self.best_model_run_id



class ModelEvaluation:


    def __init__(self,model_evaluation_config:ModelEvalConfig,
                    param_optimize_artifact:ParamOptimzeArtifact):
        
        try:
            self.param_optimize_artifact=param_optimize_artifact
            self.model_evaluation_config=model_evaluation_config

            self.saved_model_config=SavedModelConfig()
            
            self.saved_model_directory=self.saved_model_config.saved_model_dir
            
        except Exception as e:
            raise ApplicationException(e,sys)
        
        
    def save_model_and_params(self,saved_model_path, report_file_path, best_params,best_model):
        # Save the best parameters as a YAML file
        with open(report_file_path, 'w') as yaml_file:
            yaml.dump(best_params, yaml_file, default_flow_style=False)
        logging.info(f"Best model parameters saved to: {report_file_path}")

        # Save the best model
        save_object(file_path=saved_model_path,obj=best_model)
        logging.info(f"Best model saved to: {saved_model_path}")
        
    def initiate_model_evaluation(self) -> ModelEvaluationArtifact:

            logging.info(" Model Evaluation Started ")
            
            
            # Saved Model files
            saved_model_path = self.saved_model_config.saved_model_object_path
            saved_model_report_path=self.saved_model_config.saved_model_report_path
            
            
            model_evaluation_artifact=ModelEvaluationArtifact(message="Model Evaluation complete",
                                                            model_report=saved_model_path,
                                                            model_file_path=saved_model_report_path)

            return model_evaluation_artifact
        
        
    def initiate_model_evaluation_local(self) -> ModelEvaluationArtifact:
        try:
            logging.info(" Model Evaluation Started ")
            
            
            # Saved Model files
            saved_model_path = self.saved_model_config.saved_model_object_path
            saved_model_report_path=self.saved_model_config.saved_model_report_path

            logging.info(" Logging Artifacts from saved directory to Mlflow Ui ....")
            report_data=read_yaml_file(saved_model_report_path)
            experiment_name=report_data['Experiment']
            run_name=report_data['Run_name']
            
            # Mlflow Code 
            logging.info(" Mlflow ...")
            logging.info(f"Experiment : {experiment_name} , Run_name: {run_name}")
            Exp_eval=Experiments_evaluation()
            # Accessing report data dn saved model 
            saved_model=load_object(saved_model_path)
            Exp_eval.read_report(report_data=report_data,model=saved_model)
            
            # Getting best model from the Mlflow log and Saving in the Directory 
            Exp_eval.run_mlflow_experiment()    
            
     
            model_report,downloaded_model=Exp_eval.download_model_and_generate_report()
        
            # Generate a YAML file with the best model parameters
            self.save_model_and_params(saved_model_path=saved_model_path,
                                        report_file_path=saved_model_report_path,
                                        best_model=downloaded_model,
                                        best_params=model_report
                                        )
            
                                            
            model_evaluation_artifact=ModelEvaluationArtifact(message="Model Evaluation complete",
                                                            model_report=saved_model_path,
                                                            model_file_path=saved_model_report_path)

            return model_evaluation_artifact
        
        
        
 
            
        except Exception as e:
            logging.error("Error occurred during model evaluation!")
            raise ApplicationException(e, sys) from e


    def __del__(self):
        logging.info(f"\n{'*'*20} Model evaluation log completed {'*'*20}\n\n")
        
        