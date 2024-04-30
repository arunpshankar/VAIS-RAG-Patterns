from src.config.logging import logger
from src.config.setup import config
from src.generate.llm import LLM




llm = LLM()


def evaluate_factual_correctness(expected_ans: str, generated_ans: str) -> dict:
    task = """Given the expected and generated answers as shown below, compare the answers and classify them into one of the three classes - `fully correct`, `partially correct`, or `wrong`. If the answer is partially correct or wrong, provide the rationale. The output should be two things - class and rationale as a Python dictionary. For class, it should be one word ONLY (which is the expected class), and for rationale, provide the reason succinctly, especially focusing on numbers and areas where the generated answer failed to match the expected. Do NOT focus on semantics. If the units are different, normalize them before comparing."""
    response = llm.compare(task, expected_ans, generated_ans)
    return response


if __name__ == '__main__':
    expected_ans = "In Q1 of 2021, Google Cloud's operating loss was $974 million. In Q1 of 2020, Google Cloud had an operating loss of $1.73 billion."
    generated_ans = """
Google Cloud's Operating Income/Loss in Q1 2021 vs. 2020

In Q1 2021, Google Cloud reported an operating loss of **$0.974 billion**, compared to an operating loss of **$1.73 billion** in Q1 2020. This represents a **40% improvement** year-over-year. 

Here's a breakdown:

* **Q1 2021:** Operating loss of $0.974 billion
* **Q1 2020:** Operating loss of $1.73 billion

While Google Cloud remains unprofitable, the narrowing loss indicates progress towards profitability. 
"""
    response = evaluate_factual_correctness(expected_ans, generated_ans)
    print(response)
