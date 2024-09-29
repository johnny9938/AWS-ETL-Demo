import os
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from typing import Optional


def upload_directory_to_s3(local_directory: str, bucket_name: str, s3_prefix: Optional[str] = '') -> None:
    """Upload all files from a local directory to an S3 bucket."""
    s3_client = boto3.client('s3')

    for root, dirs, files in os.walk(local_directory):
        for filename in files:
            local_file_path = os.path.join(root, filename)
            # Create a relative path to maintain folder structure in S3
            relative_path = os.path.relpath(local_file_path, local_directory)
            s3_file_path = os.path.join(s3_prefix, relative_path).replace("\\", "/")  # Normalize path for S3

            try:
                s3_client.upload_file(local_file_path, bucket_name, s3_file_path)
                print(f"Uploaded {local_file_path} to s3://{bucket_name}/{s3_file_path}")
            except FileNotFoundError:
                print(f"The file {local_file_path} was not found.")
            except NoCredentialsError:
                print("Credentials not available. Ensure AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are set.")
            except PartialCredentialsError:
                print("Incomplete credentials provided.")
            except Exception as e:
                print(f"An error occurred: {e}")


def main():
    # Configuration
    local_directory = "output_logs"  # Directory containing log files
    s3_bucket_name = "yonatan-s3-bucket"  # Replace with your S3 bucket name
    s3_prefix = "raw_logs/"  # Optional: specify a prefix for S3

    # print s3 bucket address
    print(f"s3://{s3_bucket_name}/{s3_prefix}")

    upload_directory_to_s3(local_directory, s3_bucket_name, s3_prefix)


if __name__ == "__main__":
    main()
