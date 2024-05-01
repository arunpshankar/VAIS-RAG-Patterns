from src.config.logging import logger
from typing import Tuple
from typing import List 
from typing import Dict 
import pandas as pd 
import numpy as np


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


def save_retrieval_eval_results(eval_results: List[Tuple[str, str, str, str, List[str]]], output_file: str) -> None:
    """
    Save the evaluation results for retrieval to a CSV file.

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
        raise 


def save_generation_eval_results(results: pd.DataFrame, output_file: str) -> None:
    """
    Save the evaluation results stored in a DataFrame to a CSV file.

    Parameters:
    results (pd.DataFrame): A pandas DataFrame containing the evaluation results.
    output_file (str): The path string where the CSV file will be saved.
    """
    try:
        results.to_csv(output_file, index=False)
        logger.info("Results saved successfully.")
    except Exception as e:
        logger.error(f"Failed to save results: {e}")
        raise


def compute_accuracy(results: pd.DataFrame) -> Tuple[float, Dict[str, float]]:
    """
    Compute the overall accuracy of evaluation results and the proportion of each class type.
    
    Args:
    results (pd.DataFrame): A DataFrame with a column 'class' that contains the classification results
        which could be 'fully correct', 'partially correct', or 'wrong'.

    Returns:
    Tuple[float, Dict[str, float]]: A tuple containing the overall accuracy as a float and a dictionary
        with the proportion of each class type.

    Raises:
    ValueError: If the required 'class' column is missing or if there are no valid entries to compute accuracy.
    """
    try:
        score_mapping = {'fully correct': 1, 'partially correct': 0.5, 'wrong': 0}
        results['score'] = results['class'].map(score_mapping)
        accuracy = np.mean(results['score'])
        breakdown = results['class'].value_counts(normalize=True).to_dict()
        logger.info("Accuracy computed.")
        if pd.isna(accuracy):
            raise ValueError("No valid entries to compute accuracy.")
        return accuracy, breakdown
    except KeyError:
        logger.error("The DataFrame lacks the required 'class' column.")
        raise ValueError("The DataFrame lacks the required 'class' column.")
    except Exception as e:
        logger.error(f"An error occurred while computing accuracy: {e}")
        raise

