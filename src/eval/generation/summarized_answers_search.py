
from src.eval.factual_correctness import evaluate_factual_correctness
from src.eval.semantic_similarity import calculate_cosine_similarity
from src.search.doc_search import get_summarized_answer
from src.eval.semantic_similarity import embed_text
from src.config.logging import logger
from typing import Tuple
from tqdm import tqdm
import pandas as pd
import numpy as np
import time


def load_data(input_file: str) -> pd.DataFrame:
    """Load data from a CSV file, keeping only the first 5 rows."""
    try:
        df = pd.read_csv(input_file)
        df = df.head(10)
        logger.info("Data loaded successfully.")
        return df
    except Exception as e:
        logger.error(f"Failed to load data: {e}")
        raise


def save_results(results: pd.DataFrame, output_file: str):
    """Save results to a CSV file without index."""
    try:
        results.to_csv(output_file, index=False)
        logger.info("Results saved successfully.")
    except Exception as e:
        logger.error(f"Failed to save results: {e}")
        raise


def compute_accuracy(results: pd.DataFrame) -> Tuple[float, dict]:
    """Compute the overall accuracy and the breakdown by class type."""
    score_mapping = {'fully correct': 1, 'partially correct': 0.5, 'wrong': 0}
    results['score'] = results['class'].map(score_mapping)
    accuracy = np.mean(results['score'])
    breakdown = results['class'].value_counts(normalize=True).to_dict()
    logger.info("Accuracy computed.")
    return accuracy, breakdown


def evaluate_summarized_answer(data: pd.DataFrame, data_store_id: str) -> pd.DataFrame:
    """Evaluate answers by comparing predicted to expected using semantic similarity and factual correctness."""
    results = []
    for _, row in tqdm(data.iterrows(), total=data.shape[0]):
        question = row['question']
        expected_answer = row['answer']
        
        try:
            predicted_answer = get_summarized_answer(question, data_store_id)
            similarity = calculate_cosine_similarity(embed_text([expected_answer])[0], embed_text([predicted_answer])[0])
            factual_evaluation = evaluate_factual_correctness(predicted_answer, expected_answer)
            
            result = {
                'question': question,
                'expected_answer': expected_answer,
                'predicted_answer': predicted_answer,
                'semantic_similarity': similarity,
                'class': factual_evaluation['class'],
                'rationale': factual_evaluation['rationale']
            }
            results.append(result)
            time.sleep(3)
        except Exception as e:
            logger.error(f"Error processing question {question}: {e}")
            continue
    
    return pd.DataFrame(results)


def main():
    """Main function to execute the evaluation process."""
    input_file = './data/eval/ground_truth.csv'
    output_file = './data/eval/generation/summarized_answers_results.csv'
    data_store_id = "quarterly-reports"

    try:
        data = load_data(input_file)
        eval_results = evaluate_summarized_answer(data, data_store_id)
        save_results(eval_results, output_file)
        
        accuracy, breakdown = compute_accuracy(eval_results)
        with open('./data/eval/generation/summarized_answers_results_accuracy.txt', 'w') as f:
            f.write(f'Accuracy: {accuracy:.2f}\n')
            for cls, perc in breakdown.items():
                f.write(f'{cls}: {perc:.2%}\n')
        logger.info("Evaluation completed successfully.")
    except Exception as e:
        logger.error(f"An error occurred in the main function: {e}")


if __name__ == "__main__":
    main()
