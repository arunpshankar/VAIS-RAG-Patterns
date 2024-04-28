from src.config.logging import logger 
from typing import Tuple
from typing import List
import pandas as pd
import numpy as np
import os


def normalize_document_name(doc_name: str) -> str:
    return doc_name.replace(' ', '').replace('-', '').lower()


def calculate_metrics(ranked_docs: List[str], expected_doc: str) -> Tuple[float, float, float, float, float, float]:
    try:
        expected_doc_normalized = normalize_document_name(expected_doc)
        ranked_docs_normalized = [normalize_document_name(doc) for doc in ranked_docs]
        if expected_doc_normalized in ranked_docs_normalized:
            rank = ranked_docs_normalized.index(expected_doc_normalized) + 1
            p_at_1 = 1 if rank <= 1 else 0
            p_at_3 = 1 if rank <= 3 else 0
            p_at_5 = 1 if rank <= 5 else 0
            mrr = 1 / rank
            ndcg_value = ndcg([1 if doc == expected_doc_normalized else 0 for doc in ranked_docs_normalized], 5)
            ap = average_precision([1 if doc == expected_doc_normalized else 0 for doc in ranked_docs_normalized])
        else:
            p_at_1, p_at_3, p_at_5, mrr, ndcg_value, ap = 0, 0, 0, 0, 0, 0
        return p_at_1, p_at_3, p_at_5, mrr, ndcg_value, ap
    except Exception as e:
        logger.error(f"An error occurred while calculating metrics: {e}")
        return 0, 0, 0, 0, 0, 0


def calculate_recall_at_k(ranked_docs: List[str], expected_doc: str, k: int = 5) -> float:
    expected_doc_normalized = normalize_document_name(expected_doc)
    ranked_docs_normalized = [normalize_document_name(doc) for doc in ranked_docs][:k]
    recall = 1 if expected_doc_normalized in ranked_docs_normalized else 0
    return recall


def dcg(relevances: List[int], rank: int) -> float:
    relevances = np.asarray(relevances)[:rank]
    return np.sum(relevances / np.log2(np.arange(2, len(relevances) + 2)))


def ndcg(relevances: List[int], rank: int) -> float:
    best_dcg = dcg(sorted(relevances, reverse=True), rank)
    actual_dcg = dcg(relevances, rank)
    return actual_dcg / best_dcg if best_dcg else 0


def process_data_frame(data: pd.DataFrame) -> pd.DataFrame:
    data[['P@1', 'P@3', 'P@5', 'MRR', 'NDCG', 'AP', 'Recall@5']] = data.apply(
        lambda row: list(calculate_metrics(eval(row['matched_documents']), row['expected_document'])) + 
                    [calculate_recall_at_k(eval(row['matched_documents']), row['expected_document'])],
        axis=1, result_type='expand'
    )
    return data


def average_precision(relevances: List[int]) -> float:
    hits = np.where(np.array(relevances) == 1)[0] + 1  # Get indices where documents are relevant
    precisions = [1/(i+1) for i in hits]
    return np.mean(precisions) if len(precisions) > 0 else 0


def mean_average_precision(data: pd.DataFrame) -> float:
    ap_values = []
    for _, row in data.iterrows():
        relevances = [1 if normalize_document_name(doc) == normalize_document_name(row['expected_document']) else 0 for doc in eval(row['matched_documents'])]
        ap_values.append(average_precision(relevances))
    return np.mean(ap_values)


def append_averages_to_df(data: pd.DataFrame) -> pd.DataFrame:
    map_value = mean_average_precision(data)
    averages = data[['P@1', 'P@3', 'P@5', 'MRR', 'NDCG', 'Recall@5']].mean()
    averages['AP'] = map_value
    averages_df = pd.DataFrame([averages], index=['Averages'])
    return pd.concat([data, averages_df])


def save_data_to_csv(data: pd.DataFrame, directory: str, filename: str) -> None:
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, filename)
    data.to_csv(file_path, index=False)
    logger.info(f"Data saved successfully to {file_path}")


if __name__ == "__main__":
    file_path = './data/eval/01.csv'
    data = pd.read_csv(file_path)
    processed_data = process_data_frame(data)
    final_data = append_averages_to_df(processed_data)
    save_data_to_csv(final_data, './data/eval/retrieval', '01_metrics.csv')

    file_path = './data/eval/02.csv'
    data = pd.read_csv(file_path)
    processed_data = process_data_frame(data)
    final_data = append_averages_to_df(processed_data)
    save_data_to_csv(final_data, './data/eval/retrieval', '02_metrics.csv')
    logger.info("Metrics and averages saved successfully.")
