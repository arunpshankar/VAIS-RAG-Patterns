from src.generate.ner import extract_entities
from src.config.logging import logger
from typing import Optional
import re


def validate_company(company: str) -> Optional[str]:
    """
    Validates the given company name against a predefined list of valid companies.

    Args:
    company (str): The company name to validate.

    Returns:
    Optional[str]: The validated company name in lowercase if valid, otherwise None.
    """
    valid_companies = ['alphabet', 'microsoft', 'amazon']
    try:
        company = company.strip().lower()
        if company in valid_companies:
            logger.info(f"Company '{company}' is valid.")
            return company
        logger.warning(f"Company '{company}' is not valid.")
    except Exception as e:
        logger.error(f"Error validating company name: {e}")
    return None

def validate_time_period(time_period: str) -> Optional[str]:
    """
    Validates the given time period to match the expected format "Q[1-4] 20[20-23]".

    Args:
    time_period (str): The time period to validate.

    Returns:
    Optional[str]: The time period if it matches the format, otherwise None.
    """
    pattern = r'Q[1-4] 20[2][0-3]'
    try:
        if re.fullmatch(pattern, time_period.strip()):
            logger.info(f"Time period '{time_period}' is valid.")
            return time_period
        logger.warning(f"Time period '{time_period}' is not valid.")
    except Exception as e:
        logger.error(f"Error validating time period: {e}")
    return None


def extract_and_validate_entities(query: str, max_retries: int = 5) -> Tuple[str, str]:
    """
    Extracts entities from a query and validates them with a maximum number of retries.

    Parameters:
        query (str): The query from which to extract entities.
        max_retries (int): The maximum number of times to attempt validation.

    Returns:
        Tuple[str, str]: A tuple containing the validated company name and time period.

    Raises:
        ValueError: If entities cannot be validated after the specified number of attempts.
    """
    retry_count = 0
    while retry_count < max_retries:
        entities = extract_entities(query)
        company = entities.get('company', '').strip().lower()
        time_period = entities.get('time_period', '').strip()

        if validate_company(company) and validate_time_period(time_period):
            return company, time_period
        retry_count += 1
        print(f"Retry {retry_count}/{max_retries}: Validation failed, retrying...")
    
    raise ValueError("Failed to validate entities after several attempts.")