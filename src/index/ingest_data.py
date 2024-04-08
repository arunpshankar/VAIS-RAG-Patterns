from src.config.logging import logger
from src.config.setup import config
import requests


def ingest_documents(gcs_input_uri: str, data_store_id: str) -> None:
    """
    Sends a POST request to GCP to import documents into a specified data store.

    Parameters:
        gcs_input_uri (str): URI of the input document location in Google Cloud Storage.
        data_store_id (str): Identifier of the data store where documents will be imported.

    Raises:
        Exception: If the request to the GCP API fails.
    """
    # Configuration and Request Setup
    project_id = config.PROJECT_ID
    url = f"https://discoveryengine.googleapis.com/v1/projects/{project_id}/locations/global/collections/default_collection/dataStores/{data_store_id}/branches/0/documents:import"

    headers = {
        "Authorization": f"Bearer {config.ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "gcsSource": {
            "inputUris": [gcs_input_uri] 
        }    
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.exceptions.HTTPError as err:
        logger.error(f"HTTP error occurred: {err}")
        raise
    except Exception as err:
        logger.error(f"Error occurred during GCP documents import: {err}")
        raise
    else:
        logger.info("Request successful")
        logger.info(response.json())

# Example Usage
if __name__ == '__main__':
    gcs_uri = f'gs://{config.BUCKET}/raw_docs'
    data_store = 'quarterly-reports'
    ingest_documents(gcs_uri, data_store)
