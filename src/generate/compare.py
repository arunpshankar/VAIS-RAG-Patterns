from vertexai.language_models import TextEmbeddingModel
from vertexai.language_models import TextEmbeddingInput
from src.config.logging import logger
from src.config.setup import config
from typing import List 


model = TextEmbeddingModel.from_pretrained(config.TEXT_GEN_MODEL_NAME)


def embed_text(text: str, task: str = "SEMANTIC_SIMILARITY") -> List[float]:
    """Embeds texts with a pre-trained, foundational model."""
    
    embedding_input = TextEmbeddingInput(text, task) 
    embedding = model.get_embeddings(embedding_input)
    return embedding.values



if __name__ == '__main__':
    pass