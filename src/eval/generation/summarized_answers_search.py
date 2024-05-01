
from src.eval.factual_correctness import evaluate_factual_correctness
from src.eval.semantic_similarity import calculate_cosine_similarity
from src.eval.utils import save_generation_eval_results
from src.search.doc_search import get_summarized_answer
from src.eval.semantic_similarity import embed_text
from src.eval.utils import compute_accuracy
from src.config.logging import logger
from src.eval.utils import load_data
from tqdm import tqdm
import pandas as pd
import time


def evaluate_summarized_answer(data: pd.DataFrame, data_store_id: str) -> pd.DataFrame:
    """Evaluate answers by comparing predicted to expected using semantic similarity and factual correctness."""
    results = []
    for _, row in tqdm(data.iterrows(), total=data.shape[0]):
        question = row['question']
        expected_answer = row['answer']
        
        try:
            predicted_answer = get_summarized_answer(question, data_store_id)
            similarity = calculate_cosine_similarity(embed_text([expected_answer])[0], embed_text([predicted_answer])[0])
            factual_evaluation = evaluate_factual_correctness(question, expected_answer, predicted_answer)
            
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
        save_generation_eval_results(eval_results, output_file)
        
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
