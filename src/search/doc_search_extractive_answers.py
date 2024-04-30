from src.utils.validate import extract_and_validate_entities
from src.search.utils import extract_filename
from src.search.utils import filtered_search
from src.generate.qa import generate_answer
from src.config.logging import logger 
from typing import Dict 
from typing import Any
    

def get_top_extractive_answers(results: Dict[str, Any], n: int) -> str:
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
            source = extract_filename(info['link'])
            extractive_answers.append('\n\n'.join(info.get('extractive_answers', 'No answer found')) + f' Ref:[{source}]')
    except Exception as e:
        # Handle any errors that might occur
        logger.error(f"Error retrieving extractive answers: {e}")

    return '\n\n'.join(extractive_answers)


if __name__ == "__main__":
    query = "What was the operating income or loss (in billions) for Google Cloud for Q1 of 2021 compared to the previous year?"
    data_store_id = "quarterly-reports"
    # company = "amazon"
    # time_period = "Q4 2022"
    company, time_period = extract_and_validate_entities(query)
    results = filtered_search(query, company, time_period, data_store_id)
    extractive_answers = get_top_extractive_answers(results, 1)
    logger.info(f'Extractive answers: {extractive_answers}')
    ans = generate_answer(query, extractive_answers)
    logger.info(f'Ans: {ans}')
