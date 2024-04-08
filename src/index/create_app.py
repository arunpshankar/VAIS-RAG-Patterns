from src.config.logging import logger
from src.config.setup import config
from typing import Optional
from typing import Dict
from typing import Any
import requests
import json


def create_doc_search_app() -> Optional[Dict[str, Any]]:
    """
    Creates a document search application using the Google Discovery Engine API.

    This function constructs a POST request to the Google Discovery Engine API to create a
    new search engine instance for a specified document collection.

    Returns:
        dict: A dictionary containing the response data from the API if the request is successful.
        None: If the request fails.
    """
    url = f"https://discoveryengine.googleapis.com/v1alpha/projects/{config.PROJECT_ID}/locations/global/collections/default_collection/engines?engineId={config.DATA_STORE_ID}"

    # Headers for the request
    headers = {
        "Authorization": f"Bearer {config.ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "X-Goog-User-Project": config.PROJECT_ID
    }

    # Request payload
    data = {
        "displayName": config.DATA_STORE_DISPLAY_NAME,
        "dataStoreIds": [config.DATA_STORE_ID],
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
    result = create_doc_search_app()
    if result:
        logger.info(f"App creation result: {json.dumps(result, indent=2)}")
    else:
        logger.error("App creation failed.")
