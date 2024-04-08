from src.config.logging import logger
from src.config.setup import config
from typing import Dict, Any
import requests


def create_data_store() -> Dict[str, Any]:
    """
    Create a data store in GCP Vertex AI Search.

    Returns:
        Dict[str, Any]: The response from the GCP API.

    Raises:
        Exception: If the data store ID or display name already exists.
    """
    url = f"https://discoveryengine.googleapis.com/v1alpha/projects/{config.PROJECT_ID}/locations/global/collections/default_collection/dataStores?dataStoreId={config.DATA_STORE_ID}"

    headers = {
        'Authorization': f'Bearer {config.ACCESS_TOKEN}',
        'Content-Type': 'application/json',
        'X-Goog-User-Project': config.PROJECT_ID
    }

    data = {
        'displayName': config.DATA_STORE_DISPLAY_NAME,
        'industryVertical': 'GENERIC',
        'solutionTypes': ['SOLUTION_TYPE_SEARCH'],
        'contentConfig': 'CONTENT_REQUIRED',
        'searchTier': 'STANDARD',
        'searchAddOns': ['LLM']
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Specific error handling for data store ID or display name conflicts
        if response.status_code == 409:  # Assuming 409 Conflict for duplicate ID or name
            logger.error("Data store ID or display name already exists. Choose a different name or ID.")
        else:
            logger.error(f"HTTP Error occurred: {e}")
        raise
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        raise

    return response.json()

if __name__ == '__main__':
    try:
        response = create_data_store()
        print(response)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
