from src.config.logging import logger
from src.search.utils import search


def get_summarized_answer(query: str, data_store_id: str) -> str:
    """
    Executes a search query on a specified data store and returns the summarized answer.
    
    :param query: The search query string.
    :param data_store_id: The identifier for the data store to be queried.
    :return: A string containing the summarized answer.
    """
    try:
        results = search(query, data_store_id)
        summarized_answer = results.get('summarized_answer', 'No answer found.')
    except Exception as e:
        logger.error(f"Failed to retrieve summarized answer: {e}")
        return "Error retrieving data."
    return summarized_answer

if __name__ == "__main__":
    query = """What was LinkedIn's revenue increase in Q1 2021 according to Microsoft's earnings report, and what was the growth rate when adjusted for constant currency?"""
    data_store_id = "quarterly-reports"
    
    summarized_ans = get_summarized_answer(query, data_store_id)
    print(f'Summarized Answer = {summarized_ans}')
