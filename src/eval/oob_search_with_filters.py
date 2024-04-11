from src.search.doc_search_with_filters import search
from src.generate.ner import extract_entities
from src.config.logging import logger
from typing import Tuple
from typing import List
from tqdm import tqdm
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
        entities = extract_entities(question)
        company = entities['company']
        company = company.strip().lower()
        time_period = entities['time_period']

        try:
            results = search(question, company, time_period, data_store_id)
            summarized_ans = results['summarized_answer']
            match_info = results['match_info']
            matched_docs = [f"{info['company']}-{info['time_period'].lower()}" for info in match_info]
            eval_results.append((question, expected_ans, summarized_ans, expected_doc, matched_docs))
        except Exception as e:
            logger.error(f"Error processing question '{question}': {e}")
            eval_results.append((question, expected_ans, "Error in processing", expected_doc, []))
    return eval_results


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


def main():
    data_store_id = "quarterly-reports"
    file_path = './data/eval/ground_truth.csv'
    output_file = './data/eval/02.csv'
    
    data = load_data(file_path)
    eval_results = evaluate_document_search(data, data_store_id)
    save_results(eval_results, output_file)


if __name__ == "__main__":
    main()
