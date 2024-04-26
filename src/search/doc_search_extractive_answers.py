from src.search.utils import extract_relevant_data
from src.search.utils import create_summary_dict
from src.search.utils import search_data_store
from src.config.logging import logger 
from typing import Dict
from typing import List 
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
    

def get_top_extractive_answers(results: Dict[str, Any], n: int) -> List[str]:
    """
    Retrieves the top N extractive answers from the search results.

    Parameters:
    results (Dict[str, Any]): The dictionary containing the search results.
    n (int): The number of top results to retrieve.

    Returns:
    List[str]: A list of the top N extractive answers.
    """
    extractive_answers = []
    try:
        # Retrieve up to N extractive answers if they exist
        for info in results.get('match_info', [])[:n]:
            extractive_answers.append(info.get('extractive_answers', 'No answer found')[0])
    except Exception as e:
        # Handle any errors that might occur
        print(f"Error retrieving extractive answers: {e}")

    return extractive_answers


if __name__ == "__main__":
    query = "What was the operating income or loss (in billions) for Google Cloud for Q1 of 2021 compared to the previous year?"
    data_store_id = "quarterly-reports"

    results = search(query, data_store_id)
    answers = get_top_extractive_answers(results, 2)[0]
    print(answers)
