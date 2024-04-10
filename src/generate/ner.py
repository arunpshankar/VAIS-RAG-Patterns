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
    logger.info("Starting Named Entity Recognition (NER)")
    extracted_entities = {}
    
    def extract_entity(task: str, query: str) -> str:
        return llm.predict(task=task, query=query)

    extracted_entities['company'] = extract_entity('Given a query as shown below, extract the company name from it. If company name not found return NONE.', query)
    extracted_entities['time_period'] = extract_entity('Given a query as shown below, extract the time period from it. If country name not found return NONE.', query)
    logger.info("NER completed successfully!")
    return extracted_entities


if __name__ == '__main__':
    query = "Annual Report 2012 commerzbank"
    entities = extract_entities(query)
    logger.info(entities)
