import boto3
import os
from dotenv import load_dotenv

class S3Connector:
    def __init__(self):
        self.load_aws_credentials()
        self.s3_client = boto3.client('s3', aws_access_key_id=self.aws_access_key_id,
                                     aws_secret_access_key=self.aws_secret_access_key)

    def load_aws_credentials(self):
        # Load environment variables from .env file
        load_dotenv()
        AWS_ACCESS_KEY_ID='AKIAYS2NXLBTUIAATZ7L'
        AWS_SECRET_ACCESS_KEY='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'


        # Retrieve AWS credentials from environment variables
      #  self.aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
      #  self.aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        self.aws_access_key_id = AWS_ACCESS_KEY_ID
        self.aws_secret_access_key = AWS_SECRET_ACCESS_KEY

    def get_s3_client(self):
        return self.s3_client