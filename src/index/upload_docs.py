from google.oauth2.service_account import Credentials as ServiceAccountCredentials
from src.config.logging import logger
from src.config.setup import config
from google.cloud import storage
from typing import Optional, Union
from pathlib import Path


def init_client() -> Optional[storage.Client]:
    """
    Initialize the Google Cloud Storage (GCS) client using service account credentials specified in the configuration.

    Returns:
        Optional[google.cloud.storage.Client]: An initialized GCS client if the credentials and project ID are correct, None otherwise.
    """
    try:
        credentials = ServiceAccountCredentials.from_service_account_file(config.CREDENTIALS_PATH)
        client = storage.Client(credentials=credentials, project=config.PROJECT_ID)
        logger.info("GCS client initialized successfully.")
        return client
    except Exception as e:
        logger.error(f"Failed to initialize GCS client: {str(e)}")
        return None


def upload(client: storage.Client, source_file: Union[str, Path], destination_blob_name: str) -> None:
    """
    Uploads a file to the specified GCS bucket and logs the operation's success or failure.

    Args:
        client (google.cloud.storage.Client): Initialized GCS client.
        source_file (Union[str, Path]): The file path of the source file to be uploaded.
        destination_blob_name (str): The blob name for the file in the GCS bucket.

    Raises:
        ValueError: If the GCS client is not initialized.
        RuntimeError: If the file upload fails.
    """
    if not client:
        raise ValueError("GCS client is not initialized.")
    
    try:
        bucket = client.get_bucket(config.BUCKET)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(str(source_file))
        logger.info(f"Successfully uploaded {source_file} to {config.BUCKET}/{destination_blob_name}")
    except Exception as e:
        logger.error(f"Failed to upload {source_file} to GCS: {str(e)}")
        raise RuntimeError(f"Failed to upload {source_file} to GCS: {str(e)}")


if __name__ == '__main__':
    client = init_client()
    if client:
        folder_name = 'raw_docs'
        source_directory = Path('./data/raw_docs/')
        for file_path in source_directory.iterdir():
            if file_path.is_file():
                upload(client, file_path, f"{folder_name}/{file_path.name}")
