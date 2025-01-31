import boto3
import os
from botocore.client import Config
from pathlib import Path
import pyprojroot
import sys
import click

root = pyprojroot.find_root(pyprojroot.has_dir("config"))
sys.path.append(str(root))

from config import settings

@click.command()
@click.option('--prefix', type=str, default='static_crawler/processed/')
@click.option('--local_dir', type=str, default='data/raw')
def download_files(prefix: str, local_dir: str):
    """
    Download all files from a MinIO prefix/path
    Args:
        prefix: S3 prefix/path (e.g., 'static_crawler_test/processed/')
        local_dir: Local directory to save files
    """
    s3_client = boto3.client(
        's3',
        endpoint_url=settings.AWS_ENDPOINT_URL,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        config=Config(signature_version='s3v4')
    )

    # Ensure the prefix ends with '/' for directory-like behavior
    if not prefix.endswith('/'):
        prefix += '/'

    # List objects under the prefix
    response = s3_client.list_objects_v2(
        Bucket=settings.AWS_BUCKET_NAME,
        Prefix=prefix
    )

    if 'Contents' not in response:
        print(f"No files found in prefix: {prefix}")
        return

    # Create local directory if needed
    Path(local_dir).mkdir(parents=True, exist_ok=True)

    # Download each file
    for obj in response['Contents']:
        # Skip the directory marker itself
        if obj['Key'].endswith('/'):
            continue

        # Create local file path
        relative_path = os.path.relpath(obj['Key'], prefix)
        local_path = os.path.join(local_dir, relative_path)
        
        # Create parent directories if needed
        Path(local_path).parent.mkdir(parents=True, exist_ok=True)

        # Download the file
        try:
            s3_client.download_file(
                settings.AWS_BUCKET_NAME,
                obj['Key'],
                local_path
            )
            print(f"Downloaded: {obj['Key']} -> {local_path}")
        except Exception as e:
            print(f"Error downloading {obj['Key']}: {e}")

if __name__ == "__main__":
    download_files()