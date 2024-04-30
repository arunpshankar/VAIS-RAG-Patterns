from src.config.logging import logger
from src.generate.llm import LLM


llm = LLM()


def generate_answer(question: str, context: str) -> str:
    """
    Generate an answer to a given question based on the provided context.

    Args:
    question (str): The question to answer.
    context (str): The context that informs the answer.

    Returns:
    str: The predicted answer.
    """
    prompt = f"""
    Based on the following context, provide a clear and concise answer to the question below:
    Context: {context}
    Question: {question}
    """
    return llm.predict(task=prompt, query=question)

if __name__ == '__main__':
    context = "During the latest financial quarter, the company reported an increase in revenue due to expanded market operations."
    question = "What caused the company's revenue to increase in the last quarter?"
    answer = generate_answer(question, context)
    print(answer)
    logger.info(f'Question: {question}, Answer: {answer}')
