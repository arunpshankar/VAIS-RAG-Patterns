
from src.search.utils import extract_filename
from src.config.logging import logger 
from src.search.utils import search
from typing import Dict 
from typing import Any
    

def get_top_extractive_segments(results: Dict[str, Any], n: int) -> str:
    """
    Retrieves the top N extractive segments from the search results.

    Parameters:
    results (Dict[str, Any]): The dictionary containing the search results.
    n (int): The number of top results to retrieve.

    Returns:
    List[str]: A list of the top N extractive segments.
    """
    extractive_segments = []
    try:
        # Retrieve up to N extractive answers if they exist
        for info in results.get('match_info', [])[:n]:
            source = extract_filename(info['link'])
            extractive_segments.append(info.get('extractive_segments', 'No answer found')[0] + f' Ref:[{source}]')
    except Exception as e:
        # Handle any errors that might occur
        logger.error(f"Error retrieving extractive answers: {e}")

    return '\n\n'.join(extractive_segments)


if __name__ == "__main__":
    query = "What was the operating income or loss (in billions) for Google Cloud for Q1 of 2021 compared to the previous year?"
    data_store_id = "quarterly-reports"

    results = search(query, data_store_id)
    answers = get_top_extractive_segments(results, 2)
    print(answers)
