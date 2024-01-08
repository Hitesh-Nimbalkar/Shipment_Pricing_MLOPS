
import os
import logging
from shipment_pricing.logger.logging import logging
import pandas as pd
import pickle
from shipment_pricing.utils.main_utils import read_yaml_file,load_object
from shipment_pricing.constant import *
import pandas as pd
import os

config_data=read_yaml_file(CONFIG_FILE_PATH)
# Preprocessor object file label 
preprocessor_object_label=config_data[DATA_TRANSFORMATION_CONFIG_KEY][DATA_TRANSFORMATION_PREPROCESSOR_NAME_KEY]
fea_eng_object_label=config_data[DATA_TRANSFORMATION_CONFIG_KEY][DATA_TRANSFORMATION_FEA_ENG_FILE_NAME_KEY]
# Prediction Object folder label 
prediction_folder=config_data['Prediction']['prediction_object_directory']



# Feature Engineering Object File Path  
feat_eng_file_path=os.path.join(os.getcwd(),prediction_folder,fea_eng_object_label)
preprocessor_object_file_path=os.path.join(os.getcwd(),prediction_folder,preprocessor_object_label)

# Saved Model File Path 
saved_model_directory=config_data['saved_model_config']['directory']
model_file_label=config_data['saved_model_config']['model_object']
saved_model_file_path=os.path.join(saved_model_directory,model_file_label)


try:
    feat_eng = load_object(feat_eng_file_path)
    preprocessor = load_object(preprocessor_object_file_path)
    model = load_object(saved_model_file_path)
except FileNotFoundError as e:
    print(f"Error loading object: {e}")


class instance_prediction_class:
    def __init__(self,df):
        self.user_input=df
        pass
    
 
    def preprocess_input(self):
        
        # Data Framsformation 
        transformed_data=feat_eng.transform(self.user_input)
        
        
        logging.info("Transformation Complete")
        
        logging.info(f" Columns after transformation : {transformed_data.columns}")
        
        # Transforming Columns 
        preprocessed_array = preprocessor.transform(transformed_data)
        
        logging.info("Preprocessing Done ")
        
        
        return preprocessed_array

    def prediction(self, preprocessed_input):
        # Make a prediction using the pre-trained model
        predicted_expenses = model.predict(preprocessed_input)

        # Return the array of predicted prices
        return predicted_expenses

    def predict_expense(self):
        # Preprocess the input using the preprocessor
        transformed_data = self.preprocess_input()

        # Make a prediction using the pre-trained model
        predicted_expenses = self.prediction(transformed_data)

        # Round off the predicted shipment prices to two decimal places
        expense = [round(expense, 2) for expense in predicted_expenses]

        # Print the rounded predicted shipment prices
        
        print(f"Cost Prediction is :  {expense[0]}")

        return expense[0]