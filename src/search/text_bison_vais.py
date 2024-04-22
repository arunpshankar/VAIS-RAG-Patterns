from vertexai.language_models import TextGenerationModel, GroundingSource
from vertexai.language_models import GroundingSource
from src.config.logging import logger 
from src.config.setup import *
from typing import Optional
from typing import Tuple
from typing import List 


DATA_STORE_LOCATION = 'global'

MODEL_NAME = 'text-bison@002'
TEMPERATURE = 0.0
MAX_OUTPUT_TOKENS = 2048
TOP_P = 0.0  # Tokens are selected from most probable to least until the sum of their probabilities equals the top_p value.
TOP_K = 1  # # A top_k of 1 means the selected token is the most probable among all tokens.


def generate_answer_with_citations(data_store_id: str, query: str) -> Tuple[Optional[str], List[str]]:
    """Generates an answer to the provided query using a language model and
    cited sources from the specified VertexAI Datastore.

    Args:
        data_store_id: ID of the VertexAI Datastore to use for grounding.
        query: The question or prompt for the language model.

    Returns:
        A tuple containing:
            * The generated answer text (or None if an error occurs)
            * A list of titles for the cited sources.
    """

    try:
        # Model and Datastore setup (as provided in the original code)
        model = TextGenerationModel.from_pretrained(MODEL_NAME)
        grounding_source = GroundingSource.VertexAISearch(
            data_store_id=data_store_id, 
            location=DATA_STORE_LOCATION
        )

        # Parameters for response generation
        parameters = {
            "temperature": TEMPERATURE,
            "max_output_tokens": MAX_OUTPUT_TOKENS,
            "top_p": TOP_P,
            "top_k": TOP_K
        }

        # Generate the response
        response = model.predict(
            query, grounding_source=grounding_source, **parameters
        )

        logger.info(f"Answer: {response.text}")

        citations = response.grounding_metadata.citations
        titles = [citation.title for citation in citations]
        logger.info(f"Citations: {titles}")

        return response.text, titles

    except Exception as e:
        logger.exception(f"Error generating answer: {e}")
        return None, []


if __name__ == "__main__":
    data_store_id = 'quarterly-reports'
    query = 'How many Microsoft 365 Consumer subscribers were there as of Q2 2021?'

    answer, citations = generate_answer_with_citations(data_store_id, query)