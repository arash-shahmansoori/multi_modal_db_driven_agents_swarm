import os

import boto3
from dotenv import load_dotenv

load_dotenv()


def create_s3_client():
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_default_region = os.getenv("AWS_DEFAULT_REGION")

    # Initialize a session using the credentials and region from the .env file
    session = boto3.session.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_default_region,
    )

    # Using the session, create an S3 client
    s3_client = session.client("s3")

    return s3_client
