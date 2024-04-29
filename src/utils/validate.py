from typing import Optional
import re
import logging

# Set up basic configuration for logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
            logging.info(f"Company '{company}' is valid.")
            return company
        logging.warning(f"Company '{company}' is not valid.")
    except Exception as e:
        logging.error(f"Error validating company name: {e}")
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
            logging.info(f"Time period '{time_period}' is valid.")
            return time_period
        logging.warning(f"Time period '{time_period}' is not valid.")
    except Exception as e:
        logging.error(f"Error validating time period: {e}")
    return None
