from src.search.doc_search_with_filters import search
from src.generate.ner import extract_entities
from src.eval.utils import save_results
from src.config.logging import logger
from src.eval.utils import load_data
from typing import Tuple
from typing import List
from tqdm import tqdm
import pandas as pd
import re


def validate_company(company):
    valid_companies = ['alphabet', 'microsoft', 'amazon']
    company = company.strip().lower()
    if company in valid_companies:
        return company
    return ""


def validate_time_period(time_period):
    # Regex to match "Q[1-4] 20[20-23]"
    pattern = r'Q[1-4] 20[2][0-3]'
    if re.fullmatch(pattern, time_period.strip()):
        return time_period
    return ""


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
        company = validate_company(company)
        time_period = validate_time_period(time_period)
        
        try:
            results = search(question, company, time_period, data_store_id)
            summarized_ans = results['summarized_answer']
            match_info = results['match_info']
            matched_docs = []
            for info in match_info:
                company = info['company']
                time_period = info['time_period'].lower()
                time_period = time_period.lower().replace(' ', '-')
                matched_doc = f'{company}-{time_period}'
                matched_docs.append(matched_doc)
            eval_results.append((question, expected_ans, summarized_ans, expected_doc, matched_docs))
        except Exception as e:
            logger.error(f"Error processing question '{question}': {e}")
            eval_results.append((question, expected_ans, "Error in processing", expected_doc, []))
    return eval_results


def main():
    data_store_id = "quarterly-reports"
    file_path = './data/eval/ground_truth.csv'
    output_file = './data/eval/02.csv'
    
    data = load_data(file_path)
    eval_results = evaluate_document_search(data, data_store_id)
    save_results(eval_results, output_file)


if __name__ == "__main__":
    main()
