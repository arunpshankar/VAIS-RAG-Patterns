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
    prompt = """Given the query below, extract the company name from it. The company name can be either `Microsoft`, `Alphabet`, or `Amazon`. If company `LinkedIn` is found, translate to `Microsoft`."""
    extracted_entities['company'] = extract_entity(prompt, query)
    prompt = """Given a query, extract the specific time period from it. A valid time period should be in the form 'Q1 2021' only. 
Examples of invalid formats include: 'Q2 2020 to Q2 2021', Q4 2021\nQ4 2022, 'Q2 2020 - Q2 2021', 'Q2 2020, Q2 2021', and ‘Q1 2020 Q2 2020' etc. 
The extracted time period should represent only one quarter and one year, corresponding to the present vs past. 

IMPORTANT: Ignore past references when the query is comparing the present to the past. 

Examples:
Translate 'first quarter of 2020' to 'Q1 2020'.
Translate 'third quarter of fiscal year 2021' to 'Q3 2021'.
Translate 'end of Mar 2021' to 'Q1 2021'.
Translate 'ended in Sep 2022' to 'Q3 2022'.
Translate 'increase in Q2 2021 compared to Q2 2020' to 'Q2 2021'.
Translate 'change from Q2 2020 to Q2 2021' to 'Q2 2021'.
Translate 'quarter ended Dec 31 2021' to 'Q4 2021'.
Translate 'months ended March 31, 2022' to 'Q1 2022'.
Translate 'months ended March 31, 2022?' to 'Q1 2022'.
Translate 'as of September 30, 2021?' to 'Q3 2021'.
Translate 'in Q1 2022, and how does it compare to Q1 2021?' to 'Q1 2022'.
Translate 'in Q4 2021 and Q4 2022?' to 'Q4 2022'.
Translate 'twelve months ending December 31, 2022,' to 'Q4 2022'.
Translate 'for Q4 2021, Q4 2022' to 'Q4 2022'.
Translate 'six months ended December 31, 2022' to 'Q4 2022'.
Translate 'three months ended March 31, 2023' to 'Q1 2023'.
Translate 'increase from December 31, 2022, to June 30, 2023?' to 'Q2 2023'.
Translate 'during Q4 2023?' to 'Q4 2023'.
Translate 'as of Q4 2023?' to 'Q4 2023'.
Translate 'from 2020 to the end of Q4 2023?' to 'Q4 2023'."""
    extracted_entities['time_period'] = extract_entity(prompt, query)
    logger.info(f'Query = {query}')
    logger.info(f'Extracted Entities: {extracted_entities}')
    return extracted_entities


if __name__ == '__main__':
    query = "How many additional stocks did the Board of Directors of Alphabet authorize to repurchase in Q1 of 2021?"
    entities = extract_entities(query)
    logger.info(entities)
