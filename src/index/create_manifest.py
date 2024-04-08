
from google.cloud.exceptions import GoogleCloudError
from src.config.logging import logger
from src.config.setup import config
from google.cloud import storage
from typing import Optional
from typing import Dict
from typing import List
import json
import re
import os


def extract_details_from_filename(filename: str) -> Optional[Dict[str, str]]:
    """Extract company and time period from the PDF filename using regex."""
    if not filename.endswith('.pdf'):
        logger.warning(f"Skipped non-PDF file: {filename}")
        return None
    
    try:
        pattern = r'^(?P<company>[\w\-]+)-q(?P<quarter>\d)-(?P<year>\d{4})\.pdf$'
        match = re.match(pattern, filename)
        if match:
            return match.groupdict()
        else:
            logger.warning(f"Filename does not match expected pattern: {filename}")
            return None
    except re.error as e:
        logger.error(f"Regex error when processing filename {filename}: {e}")
        return None



def generate_json_data(blobs: List[storage.Blob]) -> List[str]:
    """Generate JSON formatted strings from blob metadata and filename details."""
    data_list = []
    for i, blob in enumerate(blobs, 1):
        details = extract_details_from_filename(blob.name.split('/')[-1])
        if details:
            json_data = {
                "id": str(i),
                "jsonData": json.dumps({"company": details['company'], "time_period": f"Q{details['quarter']} {details['year']}"}),
                "content": {
                    "mimeType": "application/pdf",
                    "uri": f"gs://{config.BUCKET}/{blob.name}"
                }
            }
            data_list.append(json.dumps(json_data))
        else:
            logger.info(f"Skipping blob {blob.name} due to missing details.")
    return data_list


def upload_file_to_gcs(source_file_name: str, destination_blob_name: str):
    """Uploads a file to the specified GCS bucket."""
    try:
        client = storage.Client()
        bucket = client.bucket(config.BUCKET)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file_name)
        logger.info(f"File {source_file_name} uploaded to {destination_blob_name}")
    except GoogleCloudError as e:
        logger.error(f"Failed to upload {source_file_name} to GCS: {e}")


def create_manifest():
    prefix = 'raw_docs/'

    try:
        # Initialize the Google Cloud Storage client
        client = storage.Client()
        bucket = client.bucket(config.BUCKET)
        blobs = list(bucket.list_blobs(prefix=prefix))

        # Generate JSON data
        output_data = generate_json_data(blobs)

        # Local directory and file setup
        local_dir = './data/metadata'
        os.makedirs(local_dir, exist_ok=True)
        output_file_path = os.path.join(local_dir, 'metadata.json')

        # Write data to file
        with open(output_file_path, 'w') as file:
            for item in output_data:
                file.write(item + '\n')

        logger.info(f'Data written to {output_file_path}')

        # Upload metadata.json to GCS
        upload_file_to_gcs(output_file_path, prefix + 'metadata.json')
    except Exception as e:
        logger.error(f"An error occurred: {e}")


if __name__ == '__main__':
    create_manifest()
