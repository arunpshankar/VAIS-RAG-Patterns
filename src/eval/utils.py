from src.config.logging import logger
from typing import Tuple
from typing import List 
import pandas as pd 


def load_data(file_path: str) -> pd.DataFrame:
    """
    Load CSV data from a specified file path.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    pd.DataFrame: A DataFrame containing the loaded data.
    """
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        logger.error(f"Failed to load data from {file_path}: {e}")
        raise


def save_results(eval_results: List[Tuple[str, str, str, str, List[str]]], output_file: str) -> None:
    """
    Save the evaluation results to a CSV file.

    Parameters:
    eval_results (List[Tuple[str, str, str, str, List[str]]]): The evaluation results.
    output_file (str): The path to the output CSV file.
    """
    out_df = pd.DataFrame(eval_results, columns=['question', 'expected_answer', 'generated_answer', 'expected_document', 'matched_documents'])
    try:
        out_df.to_csv(output_file, index=False)
        logger.info(f"Results saved successfully to {output_file}")
    except Exception as e:
        logger.error(f"Failed to save results to {output_file}: {e}")
