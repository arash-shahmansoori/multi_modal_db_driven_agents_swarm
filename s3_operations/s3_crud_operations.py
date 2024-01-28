from typing import NoReturn

import boto3
import requests
from botocore.client import BaseClient
from botocore.exceptions import ClientError, NoCredentialsError


def create_bucket(s3_client: BaseClient, bucket_name: str, region: str) -> bool:
    """Create an Amazon S3 bucket with a private ACL.

    Args:
        s3_client: An authenticated S3 client object.
        bucket_name: The name of the bucket to create.
        region: The region in which to create the bucket.

    Raises:
        ClientError: If the bucket could not be created.

    Returns:
        True if the bucket was created, False otherwise.
    """

    try:
        s3_client.create_bucket(
            Bucket=bucket_name, CreateBucketConfiguration={"LocationConstraint": region}
        )

        print(f"Bucket {bucket_name} created successfully.")
    except ClientError as e:
        print(f"Error: {e}")
        return False
    return True


def check_and_create_bucket(
    s3_client: BaseClient, bucket_name: str, region: str = None
) -> NoReturn:
    """
    Check if an S3 bucket with the given name exists, and if not, create it.

    Args:
        s3_client: An authenticated S3 client object.
        bucket_name: The name of the bucket to check and possibly create.
        region: The AWS region in which to create the bucket (if needed).

    Raises:
        ValueError: If there's an error in creating the bucket or if the bucket name is not valid.
        ClientError: If there's any other AWS service error.
    """

    # Try to get the bucket's location
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' already exists.")
    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "404" or error_code == "NoSuchBucket":
            # The bucket does not exist, create it
            create_bucket(s3_client, bucket_name, region)
        else:
            # Raise the error if it's something else
            raise


def list_buckets(s3_client: BaseClient) -> NoReturn:
    """Lists all S3 buckets in the AWS account.

    Args:
        s3_client: An authenticated S3 client object.

    """
    buckets = s3_client.list_buckets()
    for bucket in buckets["Buckets"]:
        print(f"Bucket Name: {bucket['Name']}")


def upload_file_to_s3(
    file_path: str,
    object_name: str,
    s3_client: BaseClient,
    bucket_name: str,
) -> bool:
    """Upload a file to an Amazon S3 bucket.

    Args:
        file_path: Path to the file.
        object_name: S3 object name.
        s3_client: An authenticated S3 client object.
        bucket_name: Target S3 bucket.

    Raises:
        FileNotFoundError: If the file was not found.
        NoCredentialsError: If credentials are not available.

    Returns:
        True if the file was uploaded, False otherwise.
    """

    try:
        s3_client.upload_file(file_path, bucket_name, object_name)
        print(f"File {file_path} uploaded to {bucket_name}/{object_name}.")
    except FileNotFoundError:
        print("The file was not found.")
        return False
    except NoCredentialsError:
        print("Credentials not available.")
        return False
    return True


def upload_file_to_s3_partition(
    file_path: str,
    partition_name: str,
    object_name: str,
    s3_client: BaseClient,
    bucket_name: str,
) -> bool:
    """Upload a file to a specified partition in an Amazon S3 bucket.

    Args:
        file_path: Full path to the file on the local filesystem.
        partition_name: The name of the partition (or 'folder') to upload the file into.
        object_name: The S3 object name within the partition.
        s3_client: An authenticated S3 client object.
        bucket_name: The name of the S3 bucket.

    Raises:
        NoCredentialsError: If credentials are not available.
        ClientError: If the file could not be uploaded.

    Returns:
        True if the file was uploaded, False otherwise.
    """

    full_object_name = f"{partition_name}/{object_name}"

    try:
        s3_client.upload_file(file_path, bucket_name, full_object_name)
        print(f"File {file_path} uploaded to {bucket_name}/{full_object_name}.")
    except NoCredentialsError:
        print("Credentials not available.")
        return False
    except ClientError as e:
        print(f"Error: {e}")
        return False
    return True


def save_image_to_s3(
    image_url: str,
    object_name: str,
    s3_client: BaseClient,
    bucket_name: str,
) -> bool:
    """
    Fetch an image from a URL and upload it to an S3 bucket.

    Args:
        image_url: The URL of the image.
        object_name: The object name in the S3 bucket.
        s3_client: An authenticated S3 client object.
        bucket_name: The name of the S3 bucket.

    Returns:
        bool: Returns True if upload was successful, False otherwise.
    """
    # Fetch the image content from the URL
    try:
        response = requests.get(image_url, stream=True)
        # This will raise an HTTPError if the HTTP request returned an unsuccessful status code
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return False

    # Upload the image content to the S3 bucket
    try:
        # Use `put_object` method for uploading a file-like object
        s3_client.put_object(Bucket=bucket_name, Key=object_name, Body=response.content)
    except NoCredentialsError as e:
        print(f"Credentials not available: {e}")
        return False
    except Exception as e:
        print(f"Error uploading to S3: {e}")
        return False

    return True


def save_image_to_s3_partition(
    image_url: str,
    partition_name: str,
    object_name: str,
    s3_client: BaseClient,
    bucket_name: str,
) -> bool:
    """
    Fetch an image from a URL and upload it to a partition within an S3 bucket.

    Args:
        image_url: The URL of the image.
        partition_name: The partition (or 'directory') within the S3 bucket.
        object_name: The object name in the S3 bucket within the specified partition.
        s3_client: An authenticated S3 client object.
        bucket_name: The name of the S3 bucket.

    Returns:
        bool: Returns True if upload was successful, False otherwise.
    """
    # Fetch the image content from the URL
    try:
        response = requests.get(image_url, stream=True)
        response.raise_for_status()  # This will raise an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return False

    # Prepare the full object name including the partition
    full_object_name = f"{partition_name}/{object_name}"

    # Upload the image content to the S3 bucket in the specified partition
    try:
        s3_client = boto3.client("s3")
        s3_client.put_object(
            Bucket=bucket_name, Key=full_object_name, Body=response.content
        )
    except NoCredentialsError as e:
        print(f"Credentials not available: {e}")
        return False
    except Exception as e:
        print(f"Error uploading to S3: {e}")
        return False

    return True


def download_file_from_s3(
    file_path: str,
    object_name: str,
    s3_client: BaseClient,
    bucket_name: str,
) -> bool:
    """Download a file from an Amazon S3 bucket.

    Args:
        file_path: Path to save the downloaded file.
        object_name: S3 object name.
        s3_client: An authenticated S3 client object.
        bucket_name: S3 bucket name.

    Raises:
        ClientError: If the file could not be downloaded.

    Returns:
        True if the file was downloaded, False otherwise.
    """

    try:
        s3_client.download_file(bucket_name, object_name, file_path)
        print(f"File {object_name} downloaded from {bucket_name} to {file_path}.")
    except ClientError as e:
        print(f"Error: {e}")
        return False
    return True


def download_file_from_s3_partition(
    local_file_path: str,
    partition_name: str,
    object_name: str,
    s3_client: BaseClient,
    bucket_name: str,
) -> bool:
    """Download a file from a specified partition in an Amazon S3 bucket.

    Args:
        local_file_path: The local path where the file will be saved after downloading.
        partition_name: The partition (or 'folder') within the bucket where the file is stored.
        object_name: The name of the file to download from the bucket.
        s3_client: An authenticated S3 client object.
        bucket_name: The name of the S3 bucket.

    Raises:
        ClientError: If the file could not be downloaded.

    Returns:
        True if the file was downloaded, False otherwise.
    """
    full_object_name = f"{partition_name}/{object_name}"

    try:
        s3_client.download_file(bucket_name, full_object_name, local_file_path)
        print(
            f"File {full_object_name} downloaded from bucket {bucket_name} to {local_file_path}."
        )
    except ClientError as e:
        print(
            f"Error downloading file {full_object_name} from bucket {bucket_name}: {e}"
        )
        return False
    return True


def delete_file_from_s3(
    s3_client: BaseClient, bucket_name: str, object_name: str
) -> bool:
    """Delete a file from an Amazon S3 bucket.

    Args:
        s3_client: An authenticated S3 client object.
        bucket_name: S3 bucket name.
        object_name: S3 object name.

    Raises:
        ClientError: If the file could not be deleted.

    Returns:
        True if the file was deleted, False otherwise.
    """

    try:
        s3_client.delete_object(Bucket=bucket_name, Key=object_name)
        print(f"File {object_name} deleted from {bucket_name}.")
    except ClientError as e:
        print(f"Error: {e}")
        return False
    return True


def delete_bucket(s3_client: BaseClient, bucket_name: str, region: str) -> bool:
    """Delete an Amazon S3 bucket.

    This function will attempt to delete all objects within the bucket before deleting the bucket itself.

    Args:
        s3_client: An authenticated S3 client object.
        bucket_name: The name of the bucket to delete.
        region: The AWS region where the bucket is located.

    Raises:
        ClientError: If the bucket could not be deleted.

    Note:
        Be cautious with this operation. Deleting a bucket is irreversible and will
        permanently remove all contents within the bucket.

    Returns:
        True if the bucket was deleted, False otherwise.
    """
    try:
        # First, we need to delete all objects and object versions in the bucket
        bucket = boto3.resource("s3", region_name=region).Bucket(bucket_name)
        bucket.object_versions.delete()

        # If the bucket has a delete marker, we need to delete it as well
        bucket.objects.all().delete()

        # Now that the bucket is empty, we can attempt to delete it
        s3_client.delete_bucket(Bucket=bucket_name)
        print(f"Bucket {bucket_name} deleted successfully.")
    except ClientError as e:
        print(f"Error: {e}")
        return False
    return True
