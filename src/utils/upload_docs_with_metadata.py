from google.oauth2.service_account import Credentials as ServiceAccountCredentials
from src.config.logging import logger
from src.config.setup import config
from google.cloud import storage
from typing import Optional
from pathlib import Path
from typing import Union
import jsonlines
import json


def initialize_gcs_client() -> Optional[storage.Client]:
    """
    Initialize the Google Cloud Storage (GCS) client using service account credentials specified in the configuration.

    Returns:
        Optional[google.cloud.storage.client.Client]: An initialized GCS client if successful, None otherwise.
    """
    try:
        credentials = ServiceAccountCredentials.from_service_account_file(config.CREDENTIALS_PATH)
        return storage.Client(credentials=credentials, project=config.PROJECT_ID)
    except Exception as e:
        logger.error(f"Failed to initialize GCS client: {e}")


def upload_to_gcs(client: storage.Client, source_file: Union[str, Path], destination_blob_name: str, writer: jsonlines.Writer, id_: str, company_name: str) -> None:
    """
    Uploads a file to the specified GCS bucket and writes metadata to a JSON lines file.

    Args:
        client (google.cloud.storage.client.Client): Initialized GCS client.
        source_file (Union[str, Path]): The file path of the source file to be uploaded.
        destination_blob_name (str): The name for the file in the GCS bucket.
        writer (jsonlines.Writer): A writer for JSON lines file to record metadata.
        id_ (str): A unique identifier for the file.
        company_name (str): The name of the company associated with the file.
    """
    try:
        bucket = client.get_bucket(config.DOC_SEARCH_BUCKET)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(str(source_file))
        logger.info(f"Successfully uploaded {source_file} to {config.DOC_SEARCH_BUCKET}/{destination_blob_name}")
        uri = f'gs://{config.DOC_SEARCH_BUCKET}/{destination_blob_name}'
        json_data = json.dumps({"company": company_name})
        metadata = {"id": str(id_), "jsonData": json_data, "content": {"mimeType": "application/pdf", "uri": uri}}
        writer.write(metadata)
    except Exception as e:
        logger.error(f"Failed to upload {source_file} to GCS: {e}")


def extract_company_name(file_path: Path) -> Optional[str]:
    """
    Extracts the company name from a given file path, assuming a specific directory structure.

    Parameters:
    file_path (Path): The file path from which to extract the company name.

    Returns:
    Optional[str]: The extracted company name if successful, None otherwise.
    """
    try:
        parts = list(file_path.parts)
        company_name_index = parts.index('pdf_files') + 1
        return parts[company_name_index]
    except Exception as e:
        logger.error(e)


def upload(pdf_folder: Union[str, Path], metadata_file_path: str) -> None:
    """
    Iterates over PDF files in the specified folder (including subdirectories) and uploads them to GCS.
    Also creates and updates a metadata file in JSON Lines format.

    Args:
        pdf_folder (Union[str, Path]): The path to the folder containing subdirectories with PDF files.
        metadata_file_path (str): The file path where the metadata in JSON Lines format will be saved.
    """
    client = initialize_gcs_client()
    writer = jsonlines.open(metadata_file_path, mode='w')

    # Use rglob to find PDFs in subdirectories
    id_ = 1
    for pdf_file in Path(pdf_folder).rglob("*.pdf"):
        destination_blob_name = pdf_file.name
        company_name = extract_company_name(pdf_file)
        upload_to_gcs(client, pdf_file, destination_blob_name, writer, id_, company_name)
        id_ += 1

    logger.info("All PDFs uploaded successfully!")
    writer.close()


def upload_json(metadata_file_path: str) -> None:
    """
    Uploads a JSON Lines file to the specified GCS bucket.

    Args:
        metadata_file_path (str): The file path of the JSON Lines file to be uploaded.
    """
    try:
        # Assuming the bucket name is stored in a config variable
        client = initialize_gcs_client()
        bucket = client.get_bucket(config.DOC_SEARCH_BUCKET)
        blob = bucket.blob('metadata.jsonl')
        
        # Set the blob's content type to JSON
        blob.content_type = 'application/json'
        blob.upload_from_filename(metadata_file_path)

        logger.info(f"Successfully uploaded JSON file {metadata_file_path} to {config.DOC_SEARCH_BUCKET}/metadata.json")
    except Exception as e:
        logger.error(f"Failed to upload JSON file {metadata_file_path} to GCS: {e}")


if __name__ == '__main__':
    # Main execution block: Uploads PDF files and their metadata to GCS.
    upload(pdf_folder='./data/output/pdf_files/', metadata_file_path='./data/output/metadata.json')
    upload_json(metadata_file_path='./data/output/metadata.json')
