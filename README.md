### Project Overview

### UI

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/2f11d54b-ad96-4202-84d6-3ca18a636c60/46c0320e-83e7-41be-bb6d-f6f554af7f35/Untitled.png)

Deployment Architecture 

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/2f11d54b-ad96-4202-84d6-3ca18a636c60/ca62e999-81c8-47b7-9032-918ba406f995/Untitled.png)

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

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/2f11d54b-ad96-4202-84d6-3ca18a636c60/0a9b144a-9259-4b86-9860-5f46adc3e9f0/Untitled.png)

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

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/2f11d54b-ad96-4202-84d6-3ca18a636c60/808de915-6ac2-48d8-95a4-b368f570f86a/Untitled.png)

### Data Ingestion

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/2f11d54b-ad96-4202-84d6-3ca18a636c60/03f47a73-be42-4f45-9a9e-93dc20a0b2b5/Untitled.png)

Data Ingestion class represents a data ingestion process that involves retrieving data from a data source, saving it in a raw data directory, and splitting it into training and test datasets.
The class code flows in following way:
Data Ingestion class takes a necessary elements and that provides the configuration settings for the data ingestion process.
It retrieves data from a data source and saves it in a raw data directory. It accesses the configuration settings to determine the location of the raw data directory and performs the necessary operations to obtain the data from the data source and saves it in the specified directory.

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/2f11d54b-ad96-4202-84d6-3ca18a636c60/c9f52448-641c-46a9-8916-00f5fd6d4686/Untitled.png)

### Data Validation

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/2f11d54b-ad96-4202-84d6-3ca18a636c60/240a2775-de07-44c9-9ed6-00a83d9efd3e/Untitled.png)

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

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/2f11d54b-ad96-4202-84d6-3ca18a636c60/d0cd1b5b-fd49-4a53-bad8-81d6aeba5c5b/Untitled.png)

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

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/2f11d54b-ad96-4202-84d6-3ca18a636c60/51d6f0c2-50a2-4b45-8e98-cc6eb3b91545/Untitled.png)

### Model Evaluation

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/2f11d54b-ad96-4202-84d6-3ca18a636c60/296f09ca-c757-4c0b-9beb-9f8dc383f3b6/Untitled.png)

The model selection process is driven by MLFlow experimentation, where the best model is chosen based on the desired metric. The saved model directory may contain earlier models and other necessary components from previous iterations.

During the evaluation process, we compare the recently trained artifact model with the previously saved models using MLflow. By leveraging this comparison, we identify the best-performing model according to the specified metric.

Once the selection is made, we save the chosen model along with its associated model object and generate a comprehensive model report. This approach ensures that we retain the most optimal model for future use, facilitating continuous improvement and efficiency in our machine learning workflows."

### Model Pusher

https://imgr.whimsical.com/object/RNF48yHL98pcYPkp8CWePw

Upon selecting the models and gathering the relevant information from the evaluation module, we proceed to push the chosen model and its corresponding report to the saved model directory. This ensures that the selected model is readily available for future prediction processes.
