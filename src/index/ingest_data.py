from src.config.logging import logger
from src.config.setup import config
import requests


def ingest_documents() -> None:
    """
    Sends a POST request to GCP to import documents into a specified data store.

    Raises:
        Exception: If the request to the GCP API fails.
    """
    # Configuration and Request Setup
    url = f"https://discoveryengine.googleapis.com/v1/projects/{config.PROJECT_ID}/locations/global/collections/default_collection/dataStores/{config.DATA_STORE_ID}/branches/0/documents:import"

    headers = {
        "Authorization": f"Bearer {config.ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "gcsSource": {
            "inputUris": [config.GCS_INPUT_URI] 
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
    ingest_documents()
