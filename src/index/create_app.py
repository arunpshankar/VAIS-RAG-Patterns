from src.config.logging import logger
from src.config.setup import config
from typing import Optional
from typing import Dict
from typing import Any
import requests
import json


def create_doc_search_app(data_store_display_name: str, data_store_id: str) -> Optional[Dict[str, Any]]:
    """
    Creates a document search application using the Google Discovery Engine API.

    Parameters:
        data_store_display_name (str): The display name for the data store.
        data_store_id (str): The ID for the data store.

    Returns:
        dict: A dictionary containing the response data from the API if the request is successful.
        None: If the request fails.
    """
    url = f"https://discoveryengine.googleapis.com/v1alpha/projects/{config.PROJECT_ID}/locations/global/collections/default_collection/engines?engineId={data_store_id}"

    # Headers for the request
    headers = {
        "Authorization": f"Bearer {config.ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "X-Goog-User-Project": config.PROJECT_ID
    }

    # Request payload
    data = {
        "displayName": data_store_display_name,
        "dataStoreIds": [data_store_id],
        "solutionType": "SOLUTION_TYPE_SEARCH"
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        logger.info("Document search app created successfully.")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to create document search app: {str(e)}")
        return None
    

if __name__ == '__main__':
    display_name = "quarterly-reports"
    store_id = "quarterly-reports"
    result = create_doc_search_app(display_name, store_id)
    if result:
        logger.info(f"App creation result: {json.dumps(result, indent=2)}")
    else:
        logger.error("App creation failed.")