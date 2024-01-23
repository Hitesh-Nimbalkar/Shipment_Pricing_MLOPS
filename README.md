### Project Overview

### UI

![Untitled](https://github.com/Hitesh-Nimbalkar/Shipment_Pricing_MLOPS/assets/109200332/4da4d7f0-d623-4b0e-91ca-4abc7799e6c1)


Deployment Architecture 

![github actions](https://github.com/Hitesh-Nimbalkar/Shipment_Pricing_MLOPS/assets/109200332/34520d64-2741-4b2f-b636-fe4a7b262838)


### Tools used

Vscode , Mlflow, Docker, dvc, Github , python , Github actions

### Data Base

Mongo Db 

### Code Orchestration

GitHub provides features such as version tracking, collaboration tools, issue tracking, and more. Used to manage and coordinate work on projects, making it easier to track changes, collaborate with others, and ensure the stability and integrity of the codebase.

### **ML_Ops Tools**

**GitHub Actions:**

- Enables continuous integration and development directly within GitHub repositories.
- Automates tasks such as building, testing, and deploying code.
- Provides a flexible and customizable workflow for various development and deployment scenarios.
- Enhances collaboration by automating repetitive tasks and ensuring code quality.

![CICD](https://github.com/Hitesh-Nimbalkar/Shipment_Pricing_MLOPS/assets/109200332/10b741c2-9b04-4ad4-9682-8cc2846d71ff)

**DVC (Data Version Control):**

- Manages version control for datasets.
- Orchestrates and reproduces data processing pipelines.
- Facilitates efficient collaboration and sharing of workflows.
- Optimizes storage by implementing a lightweight versioning system.

**Mlflow:**

- Primarily used for machine learning experimentation.
- Supports hyperparameter tuning for optimizing model performance.
- Streamlines model deployment in various production environments.

**Docker:**

- Facilitates containerization, bundling applications and their dependencies.
- Ensures consistency across different environments, making it easier to deploy and scale applications.

### Problem statement

The objective is to predict the shipment costs of medical supplies to various countries worldwide. This constitutes a regression problem statement.

### Target Variable

Freight Cost ( USD)

### Metric Used

R2 Score

## **Training Pipeline**
![terianing pipeline](https://github.com/Hitesh-Nimbalkar/Shipment_Pricing_MLOPS/assets/109200332/86af3a65-3dfa-4322-b4f7-96f41ba35694)

\
### Data Ingestion
![Data Ingstion](https://github.com/Hitesh-Nimbalkar/Shipment_Pricing_MLOPS/assets/109200332/8524514b-8add-41a9-99d2-0adffd721f80)


![Data Ingestion](https://github.com/Hitesh-Nimbalkar/Shipment_Pricing_MLOPS/assets/109200332/910eca00-13dd-4a09-8e9e-34ec516b2807)


Data Ingestion class represents a data ingestion process that involves retrieving data from a data source, saving it in a raw data directory, and splitting it into training and test datasets.
The class code flows in following way:
Data Ingestion class takes a necessary elements and that provides the configuration settings for the data ingestion process.
It retrieves data from a data source and saves it in a raw data directory. It accesses the configuration settings to determine the location of the raw data directory and performs the necessary operations to obtain the data from the data source and saves it in the specified directory.

### Data Validation

![Data Validation](https://github.com/Hitesh-Nimbalkar/Shipment_Pricing_MLOPS/assets/109200332/07f40ed5-6f25-40f2-9be2-89051367881c)


This method aims to validate the training and test data stored in the artifact folder as a result of the data ingestion process carried out earlier. Its responsibility is to perform validation checks on the training and test datasets.
The method follows a series of steps to validate the data and logs the validation process. If the validation is successful, it exports the validated datasets to specified paths and returns the paths. However, if the validation fails, it raises an exception.
Validation processes :
●	File name of the downloaded dataset
●	Column labels
●	Validating Data types
●	Missing values whole column
●	Replace null values
Each of these methods returns a boolean value as the result of the validation. If the dataset passes all the checks and evaluates to True, it is stored in the artifact folder.
Throughout the process, the class handles any exceptions that may occur and raises an application exception with an appropriate error message.

### Data Transformation

![Data Transformation](https://github.com/Hitesh-Nimbalkar/Shipment_Pricing_MLOPS/assets/109200332/e4f2b976-4c69-4e18-94b6-c866c40469fd)


Once the validated data is obtained from the artifact folder, it proceeds for the necessary transformations before being used for model training. These transformations ensure that the data is in a suitable format and structure for the training process.

**Feature Engineering**
The feature engineering class leverages insights from exploratory data analysis (EDA) to transform the dataset, enriching it with new and meaningful information. These engineered features have the potential to improve the model's performance and predictive capacity.
To ensure consistent utilization of these features, a feature engineering object file is created, allowing for batch prediction on new data without repeating the entire feature engineering process. This approach promotes consistency, reproducible, and efficient application of pre_processing steps to the data.

**Preprocessing Pipeline**
After feature engineering the data, the next step is pre_processing . The pre_processing pipeline applies a series of steps to the training and testing datasets, ensuring they are in a consistent and suitable format for model training.
The pre_processing pipeline plays a critical role in optimizing the data for model training by standardizing and cleaning it. This enables the model to learn patterns effectively during training and make accurate predictions.

Overall, the data transformation stage ensures that the validated data undergoes necessary transformations, while feature engineering enhances the dataset by creating new features. The pre-processing pipeline then applies a series of standardized steps to prepare the data for model training.

**Output**

Object Files

Feature Engineering Pipeline ---> pkl object

Pre_processing pipeline ---> pkl object

Data Files 

Transformed Data
Train Data , Test Data

### Model Training

![Model Traiing](https://github.com/Hitesh-Nimbalkar/Shipment_Pricing_MLOPS/assets/109200332/c2f51de7-e8e0-42f1-9076-df11dc46760a)


### Model Evaluation

![Model Evaluation](https://github.com/Hitesh-Nimbalkar/Shipment_Pricing_MLOPS/assets/109200332/be035c27-54c2-446d-8ff6-b997ff1ae8c1)


The model selection process is driven by MLFlow experimentation, where the best model is chosen based on the desired metric. The saved model directory may contain earlier models and other necessary components from previous iterations.

During the evaluation process, we compare the recently trained artifact model with the previously saved models using MLflow. By leveraging this comparison, we identify the best-performing model according to the specified metric.

Once the selection is made, we save the chosen model along with its associated model object and generate a comprehensive model report. This approach ensures that we retain the most optimal model for future use, facilitating continuous improvement and efficiency in our machine learning workflows."

### Model Pusher

![Model Pusher](https://github.com/Hitesh-Nimbalkar/Shipment_Pricing_MLOPS/assets/109200332/16aab67c-34d4-4835-906c-f8fe35b48873)


Upon selecting the models and gathering the relevant information from the evaluation module, we proceed to push the chosen model and its corresponding report to the saved model directory. This ensures that the selected model is readily available for future prediction processes.
