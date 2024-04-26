from src.search.utils import extract_relevant_data
from src.search.utils import create_summary_dict
from src.search.utils import search_data_store
from src.config.logging import logger 
from typing import Dict
from typing import Any


def search(query: str, data_store_id: str) -> Dict[str, Any]:
    """
    Searches a data store based on a given search query and brand, 
    then consolidates the results in a dictionary.

    Parameters:
    query (str): The query used for searching the data store.
    data_store_id (str): Vertex AI Search Data Store ID.

    Returns:
        Dict[str, Any]: A dictionary containing the consolidated results of the search.
                        Returns an empty dictionary if an error occurs.
    """
    try:
        # Perform the search with the provided query and filter
        hits = search_data_store(query, data_store_id)

        # Extract relevant data from the search results
        matches = extract_relevant_data(hits)

        # Create a summary dictionary from the matches
        summary_dict = create_summary_dict(matches)

        return summary_dict

    except Exception as e:
        # Log the error and return an empty dictionary or an error message
        logger.error(f"Error executing search_data_store: {e}")
        return {}
    

if __name__ == "__main__":
    query = "What was the operating income or loss (in billions) for Google Cloud for Q1 of 2021 compared to the previous year?"
    data_store_id = "quarterly-reports"

    results = search(query, data_store_id)
    summarized_ans = results['summarized_answer']
    print(f'Summarized Answer = {summarized_ans}')
    print()
    match_info = results['match_info']
    for item in match_info:
        print(item)
        print('-' * 100)
