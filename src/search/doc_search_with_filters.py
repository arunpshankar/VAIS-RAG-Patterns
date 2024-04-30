from src.utils.validate import extract_and_validate_entities
from src.search.utils import filtered_search
from src.config.logging import logger


def get_filtered_summarized_answer(query: str, company: str, time_period: str, data_store_id: str) -> dict:
    """
    Executes a search query on a specified data store with filtering based on company and time period, and returns the summarized answer and match information.
    
    :param query: The search query string.
    :param company: The company to filter the search by.
    :param time_period: The time period to filter the search by.
    :param data_store_id: The identifier for the data store to be queried.
    :return: A dictionary containing the 'summarized_answer' and 'match_info'.
    """
    try:
        results = filtered_search(query, company, time_period, data_store_id)
        if 'summarized_answer' in results and 'match_info' in results:
            return {
                'summarized_answer': results['summarized_answer'],
                'match_info': results['match_info']
            }
        else:
            return {'summarized_answer': 'No answer found.', 'match_info': []}
    except Exception as e:
        logger.error(f"Failed to retrieve data: {e}")
        return {'summarized_answer': "Error retrieving data.", 'match_info': []}
    

if __name__ == "__main__":
    query = "What was the operating income or loss (in billions) for Google Cloud for Q1 of 2021 compared to the previous year?"
    data_store_id = "quarterly-reports"
    # company = "amazon"
    # time_period = "Q4 2022"
    company, time_period = extract_and_validate_entities(query)
    results = get_filtered_summarized_answer(query, company, time_period, data_store_id)
    summarized_ans = results['summarized_answer']
    print(f'Summarized Answer = {summarized_ans}')
