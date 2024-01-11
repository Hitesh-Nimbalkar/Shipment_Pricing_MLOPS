import os
from src.shipment_pricing.data_access.aws_connect import S3Connector
from src.shipment_pricing.constant import *
from src.shipment_pricing.utils.main_utils import read_yaml_file
import os
from dotenv import load_dotenv


def delete_all_files_in_bucket(bucket_name):
    """
    Deletes all files in an S3 bucket.

    Parameters:
    - bucket_name: Name of the S3 bucket
    """
    try:
        s3_connector = S3Connector()
        s3_client = s3_connector.get_s3_client()

        # List all objects in the bucket and delete them
        objects_to_delete = s3_client.list_objects_v2(Bucket=bucket_name)['Contents']
        for obj in objects_to_delete:
            s3_client.delete_object(Bucket=bucket_name, Key=obj['Key'])
    except Exception as e:
        print(f"An error occurred: {e}")

def upload_folder_to_specific_folder_in_s3(local_folder_path, bucket_name, destination_folder):
    """
    Uploads a local folder to a specific folder in an S3 bucket.

    Parameters:
    - local_folder_path: Local path of the folder to upload
    - bucket_name: Name of the S3 bucket
    - destination_folder: Name of the destination folder in the S3 bucket
    """
    # Create an S3 client
    s3_connector = S3Connector()
    s3_client = s3_connector.get_s3_client()

    # Walk through the local folder and upload files to the specific folder in S3
    for root, dirs, files in os.walk(local_folder_path):
        for file in files:
            local_file_path = os.path.join(root, file)
            s3_key = os.path.join(destination_folder, os.path.relpath(local_file_path, local_folder_path))

            # Upload the file to S3 with the specific folder structure
            s3_client.upload_file(local_file_path, bucket_name, s3_key)

def download_s3_bucket(bucket_name, local_folder):
    # Initialize the S3 client
    s3_connector = S3Connector()
    s3_client = s3_connector.get_s3_client()

    # List all objects in the bucket
    objects = s3_client.list_objects(Bucket=bucket_name)['Contents']

    # Create the local folder if it doesn't exist
    if not os.path.exists(local_folder):
        os.makedirs(local_folder)

    # Download each object
    for obj in objects:
        key = obj['Key']
        local_file_path = os.path.join(local_folder, key)  # Preserve the subfolder structure

        # Create local subfolders if they don't exist
        local_subfolder = os.path.dirname(local_file_path)
        if not os.path.exists(local_subfolder):
            os.makedirs(local_subfolder)

        # Download the object
        s3_client.download_file(bucket_name, key, local_file_path)

    print(f"Downloaded {len(objects)} objects from {bucket_name} to {local_folder}")





if __name__ == "__main__":
    
    saved_directory = os.path.join(ROOT_DIR,'Saved_model')
    preprocessor=os.path.join(ROOT_DIR,'preprocessor')
    
    
    config_data=read_yaml_file(CONFIG_FILE_PATH)
    s3_bucket_name = config_data[AWS_CONFIG_KEY][S3_BUCKET][BUCKET_NAME]
    
  #  s3_folder_key = "path/in/s3/folder"  # The prefix in S3 where you want to download files
  #  local_destination_path = "/path/to/local/downloaded_folder"
    delete_all_files_in_bucket(s3_bucket_name)
    # Upload a local folder to S3
    upload_folder_to_specific_folder_in_s3(local_folder_path=saved_directory, bucket_name=s3_bucket_name,destination_folder='Saved_model')
    upload_folder_to_specific_folder_in_s3(local_folder_path=preprocessor, bucket_name=s3_bucket_name,destination_folder='preprocessor')

