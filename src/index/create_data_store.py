from src.config.logging import logger
from src.config.setup import config
from typing import Dict, Any
import requests


def create_data_store(data_store_display_name: str, data_store_id: str) -> Dict[str, Any]:
    """
    Create a data store in GCP Vertex AI Search with a specified display name and ID.

    Args:
        data_store_display_name (str): The display name for the new data store.
        data_store_id (str): The unique identifier for the new data store.

    Returns:
        Dict[str, Any]: The response from the GCP API.

    Raises:
        Exception: If the data store ID or display name already exists.
    """
    url = f"https://discoveryengine.googleapis.com/v1alpha/projects/{config.PROJECT_ID}/locations/global/collections/default_collection/dataStores?dataStoreId={data_store_id}"

    headers = {
        'Authorization': f'Bearer {config.ACCESS_TOKEN}',
        'Content-Type': 'application/json',
        'X-Goog-User-Project': config.PROJECT_ID
    }

    data = {
        'displayName': data_store_display_name,
        'industryVertical': 'GENERIC',
        'solutionTypes': ['SOLUTION_TYPE_SEARCH'],
        'contentConfig': 'CONTENT_REQUIRED',
        'searchTier': 'ENTERPRISE',
        'searchAddOns': ['LLM']
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 409:
            logger.error("Data store ID or display name already exists. Choose a different name or ID.")
        else:
            logger.error(f"HTTP Error occurred: {e}")
        raise
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        raise

    return response.json()


if __name__ == '__main__':
    display_name = 'quarterly-reports'
    store_id = 'quarterly-reports'
    try:
        response = create_data_store(display_name, store_id)
        print(response)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
