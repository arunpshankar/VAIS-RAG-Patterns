from src.search.doc_search import search
from src.eval.utils import save_results
from src.config.logging import logger
from src.eval.utils import load_data

from typing import Tuple
from typing import List
from tqdm import tqdm
import pandas as pd


def evaluate_document_search(data: pd.DataFrame, data_store_id: str) -> List[Tuple[str, str, str, str, List[str]]]:
    """
    Evaluate the document search function against a DataFrame of questions and expected answers.

    Parameters:
    data (pd.DataFrame): The DataFrame with columns 'question', 'answer', 'document'.
    data_store_id (str): The identifier for the data store where documents are searched.

    Returns:
    List[Tuple[str, str, str, str, List[str]]]: A list of tuples containing the evaluation results.
    """
    eval_results = []
    for _, row in tqdm(data.iterrows(), total=data.shape[0], desc="Evaluating document search"): 
        question = row['question']
        expected_ans = row['answer']
        expected_doc = row['document']
        try:
            results = search(question, data_store_id)
            summarized_ans = results['summarized_answer']
            match_info = results['match_info']
            matched_docs = [f"{info['company']}-{info['time_period'].lower()}" for info in match_info]
            eval_results.append((question, expected_ans, summarized_ans, expected_doc, matched_docs))
        except Exception as e:
            logger.error(f"Error processing question '{question}': {e}")
            eval_results.append((question, expected_ans, "Error in processing", expected_doc, []))
    return eval_results


def main():
    data_store_id = "quarterly-reports"
    file_path = './data/eval/ground_truth.csv'
    output_file = './data/eval/01.csv'
    
    data = load_data(file_path)
    eval_results = evaluate_document_search(data, data_store_id)
    save_results(eval_results, output_file)


if __name__ == "__main__":
    main()
