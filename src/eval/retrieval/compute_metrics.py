from src.config.logging import logger 
from typing import Tuple
from typing import List
import pandas as pd
import numpy as np
import os


def normalize_document_name(doc_name: str) -> str:
    """
    Normalize a document name by removing spaces and hyphens and converting to lowercase.

    Args:
    doc_name (str): The original document name.

    Returns:
    str: The normalized document name.
    """
    return doc_name.replace(' ', '').replace('-', '').lower()


def calculate_metrics(ranked_docs: List[str], expected_doc: str) -> Tuple[float, ...]:
    """
    Calculate various information retrieval metrics for a given list of documents.

    Args:
    ranked_docs (List[str]): A list of document names.
    expected_doc (str): The name of the expected document.

    Returns:
    Tuple[float, ...]: A tuple containing Precision@1, Precision@3, Precision@5, MRR, NDCG, and Average Precision values.
    """
    try:
        expected_doc_normalized = normalize_document_name(expected_doc)
        ranked_docs_normalized = [normalize_document_name(doc) for doc in ranked_docs]

        if expected_doc_normalized in ranked_docs_normalized:
            rank = ranked_docs_normalized.index(expected_doc_normalized) + 1
            p_at_1 = 1 if rank == 1 else 0
            p_at_3 = 1 if rank <= 3 else 0
            p_at_5 = 1 if rank <= 5 else 0
            mrr = 1 / rank
            ndcg_value = ndcg([1 if doc == expected_doc_normalized else 0 for doc in ranked_docs_normalized], 5)
            ap = average_precision([1 if doc == expected_doc_normalized else 0 for doc in ranked_docs_normalized])
        else:
            p_at_1, p_at_3, p_at_5, mrr, ndcg_value, ap = 0, 0, 0, 0, 0, 0

        return p_at_1, p_at_3, p_at_5, mrr, ndcg_value, ap
    except Exception as e:
        logger.error(f"Error calculating metrics: {e}", exc_info=True)
        return 0, 0, 0, 0, 0, 0


def calculate_recall_at_k(ranked_docs: List[str], expected_doc: str, k: int = 5) -> float:
    """
    Calculate recall at position k for a list of documents.

    Args:
    ranked_docs (List[str]): A list of document names.
    expected_doc (str): The name of the expected document.
    k (int): The rank position up to which recall should be calculated.

    Returns:
    float: The recall value at position k.
    """
    expected_doc_normalized = normalize_document_name(expected_doc)
    ranked_docs_normalized = [normalize_document_name(doc) for doc in ranked_docs][:k]
    return 1 if expected_doc_normalized in ranked_docs_normalized else 0


def dcg(relevances: List[int], rank: int) -> float:
    """
    Calculate the Discounted Cumulative Gain (DCG) at a given rank.

    Args:
    relevances (List[int]): A list indicating the relevance scores of documents.
    rank (int): The rank position up to which DCG should be calculated.

    Returns:
    float: The DCG value.
    """
    relevances = np.asarray(relevances)[:rank]
    return np.sum(relevances / np.log2(np.arange(2, len(relevances) + 2)))


def ndcg(relevances: List[int], rank: int) -> float:
    """
    Calculate the Normalized Discounted Cumulative Gain (NDCG) at a given rank.

    Args:
    relevances (List[int]): A list indicating the relevance scores of documents.
    rank (int): The rank position up to which NDCG should be calculated.

    Returns:
    float: The NDCG value.
    """
    best_dcg = dcg(sorted(relevances, reverse=True), rank)
    actual_dcg = dcg(relevances, rank)
    return actual_dcg / best_dcg if best_dcg else 0


def process_data_frame(data: pd.DataFrame) -> pd.DataFrame:
    """
    Process the DataFrame by applying metrics calculation and recall calculation to each row.

    Args:
    data (pd.DataFrame): The input DataFrame containing the matched and expected documents.

    Returns:
    pd.DataFrame: The DataFrame with added columns for the various metrics and recall.
    """
    try:
        data[['P@1', 'P@3', 'P@5', 'MRR', 'NDCG', 'AP', 'Recall@5']] = data.apply(
            lambda row: list(calculate_metrics(eval(row['matched_documents']), row['expected_document'])) +
                        [calculate_recall_at_k(eval(row['matched_documents']), row['expected_document'])],
            axis=1, result_type='expand'
        )
        return data
    except Exception as e:
        logger.error(f"Error processing DataFrame: {e}", exc_info=True)
        return pd.DataFrame()  # Returning an empty DataFrame in case of error


def average_precision(relevances: List[int]) -> float:
    """
    Calculate the Average Precision (AP) for a list of binary relevances.

    Args:
    relevances (List[int]): A binary list where 1 indicates relevance and 0 indicates non-relevance.

    Returns:
    float: The average precision score.
    """
    try:
        hits = np.where(np.array(relevances) == 1)[0] + 1  # positions of relevant docs (1-based index)
        precisions = [1 / idx for idx in hits]
        return np.mean(precisions) if precisions else 0
    except Exception as e:
        logger.error(f"Error calculating average precision: {e}", exc_info=True)
        return 0


def mean_average_precision(data: pd.DataFrame) -> float:
    """
    Calculate the Mean Average Precision (MAP) for the entire DataFrame.

    Args:
    data (pd.DataFrame): The DataFrame containing matched documents and their expected document.

    Returns:
    float: The mean of the average precision scores for all the rows in the DataFrame.
    """
    try:
        ap_values = []
        for _, row in data.iterrows():
            relevances = [1 if normalize_document_name(doc) == normalize_document_name(row['expected_document']) else 0
                          for doc in eval(row['matched_documents'])]
            ap_values.append(average_precision(relevances))
        return np.mean(ap_values) if ap_values else 0
    except Exception as e:
        logger.error(f"Error calculating mean average precision: {e}", exc_info=True)
        return 0


def append_averages_to_df(data: pd.DataFrame) -> pd.DataFrame:
    """
    Append a row of average metric values to the bottom of the DataFrame.

    Args:
    data (pd.DataFrame): The DataFrame with individual metric values for each document set.

    Returns:
    pd.DataFrame: The DataFrame with an additional row showing the averages of the metrics.
    """
    try:
        map_value = mean_average_precision(data)
        averages = data[['P@1', 'P@3', 'P@5', 'MRR', 'NDCG', 'Recall@5']].mean()
        averages['AP'] = map_value
        averages_df = pd.DataFrame([averages], index=['Averages'])
        return pd.concat([data, averages_df])
    except Exception as e:
        logger.error(f"Error appending averages to DataFrame: {e}", exc_info=True)
        return data  # Returning the original DataFrame in case of error


def save_data_to_csv(data: pd.DataFrame, directory: str, filename: str) -> None:
    """
    Save the processed DataFrame to a CSV file.

    Args:
    data (pd.DataFrame): The DataFrame to save.
    directory (str): The directory where the CSV file will be saved.
    filename (str): The name of the CSV file.

    """
    try:
        os.makedirs(directory, exist_ok=True)
        file_path = os.path.join(directory, filename)
        data.to_csv(file_path, index=False)
        logger.info(f"Data saved successfully to {file_path}")
    except Exception as e:
        logger.error(f"Error saving data to CSV: {e}", exc_info=True)


def process_and_save_data(file_path, output_dir, output_filename):
    data = pd.read_csv(file_path)
    processed_data = process_data_frame(data)
    final_data = append_averages_to_df(processed_data)
    save_data_to_csv(final_data, output_dir, output_filename)
    logger.info(f"Metrics and averages for {output_filename} saved successfully.")


if __name__ == "__main__":
    process_and_save_data('./data/eval/01.csv', './data/eval/retrieval', '01_metrics.csv')
    process_and_save_data('./data/eval/02.csv', './data/eval/retrieval', '02_metrics.csv')