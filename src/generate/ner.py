from src.config.logging import logger
from src.generate.llm import LLM
from typing import Dict


llm = LLM()


def extract_entities(query: str) -> Dict[str, str]:
    """
    Extract key entities from the given query.

    Args:
    query (str): The input query from which information is to be extracted.

    Returns:
    Dict[str, str]: A dictionary containing extracted entities like company and time period.
    """
    extracted_entities = {}
    
    def extract_entity(task: str, query: str) -> str:
        return llm.predict(task=task, query=query)
    prompt = """Given the query below, extract the company name from it. The company name can be either Microsoft, Alphabet, or Amazon."""
    extracted_entities['company'] = extract_entity(prompt, query)
    prompt = """Given a query, extract the specific time period from it. A valid time period should be in the form 'Q1 2021' only. 
Examples of invalid formats include: 'Q2 2020 to Q2 2021', 'Q2 2020 - Q2 2021', 'Q2 2020, Q2 2021', and ‘Q1 2020 Q2 2020' etc. 
The extracted time period should represent only one quarter and one year, corresponding to the present. 
IMPORTANT: Ignore past references when the query is comparing the present to the past. 
Translate 'first quarter of 2020' to 'Q1 2020'.
Translate 'third quarter of fiscal year 2021' to 'Q3 2021'."""
    extracted_entities['time_period'] = extract_entity(prompt, query)
    logger.info(f'Query = {query}')
    logger.info(f'Extracted Entities: {extracted_entities}')
    return extracted_entities


if __name__ == '__main__':
    query = "How many additional stocks did the Board of Directors of Alphabet authorize to repurchase in Q1 of 2021?"
    entities = extract_entities(query)
    logger.info(entities)
