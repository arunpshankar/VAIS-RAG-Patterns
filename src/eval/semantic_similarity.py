from vertexai.language_models import TextEmbeddingModel, TextEmbeddingInput
from sklearn.metrics.pairwise import cosine_similarity
from src.config.logging import logger
from src.config.setup import config
from typing import List
import numpy as np


model = TextEmbeddingModel.from_pretrained(config.TEXT_EMBED_MODEL_NAME)


def embed_text(texts: List[str], task: str = "SEMANTIC_SIMILARITY") -> List[np.ndarray]:
    """Embeds texts using a pre-trained foundation model.

    Args:
        texts: A list of strings to embed.
        task: The task type for embedding (defaults to "SEMANTIC_SIMILARITY").

    Returns:
        A list of numpy arrays, where each array represents the embedding for a text.
    """
    try:
        inputs = [TextEmbeddingInput(text, task) for text in texts]
        embeddings = model.get_embeddings(inputs)
        return [embedding.values for embedding in embeddings]
    except Exception as e:
        logger.error(f"Error embedding text: {e}")
        raise  # Re-raise the exception after logging for higher-level handling


def calculate_cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """Calculates the cosine similarity between two embedding vectors.

    Args:
        vec1: The first embedding vector.
        vec2: The second embedding vector.

    Returns:
        The cosine similarity between the two vectors.
    """
    try:
        return round(cosine_similarity([vec1], [vec2])[0][0], 4)  # Directly compute without extra conversion
    except Exception as e:
        logger.error(f"Error calculating cosine similarity: {e}")
        raise  # Ensure error propagation


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
    
    expected_ans_embedding = embed_text([expected_ans])[0]
    generated_ans_embedding = embed_text([generated_ans])[0]

    similarity = calculate_cosine_similarity(expected_ans_embedding, generated_ans_embedding)
    logger.info(f"Cosine Similarity: {similarity}")
