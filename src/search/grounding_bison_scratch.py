from typing import Optional

import vertexai
from vertexai.language_models import (
    GroundingSource,
    TextGenerationModel,
    TextGenerationResponse,
)
from src.config.setup import config


def grounding(
    project_id: str,
    location: str,
    data_store_location: Optional[str],
    data_store_id: Optional[str],
) -> TextGenerationResponse:
    """Grounding example with a Large Language Model"""

    vertexai.init(project=project_id, location=location)

    # TODO developer - override these parameters as needed:
    parameters = {
        "temperature": 0.0,  # Temperature controls the degree of randomness in token selection.
        "max_output_tokens": 256,  # Token limit determines the maximum amount of text output.
        "top_p": 0.8,  # Tokens are selected from most probable to least until the sum of their probabilities equals the top_p value.
        "top_k": 40,  # A top_k of 1 means the selected token is the most probable among all tokens.
    }

    model = TextGenerationModel.from_pretrained("text-bison@002")

    if data_store_id and data_store_location:
        # Use Vertex AI Search data store
        grounding_source = GroundingSource.VertexAISearch(
            data_store_id=data_store_id, location=data_store_location
        )
    else:
        # Use Google Search for grounding (Private Preview)
        grounding_source = GroundingSource.WebSearch()

    response = model.predict(
        "What were Amazon's basic earnings per share (EPS) for Q4 2021, Q4 2022, the full year of 2021, and the full year of 2022?",
        grounding_source=grounding_source,
        **parameters,
    )
    print(f"Response from Model: {response.text}")
    print(f"Grounding Metadata: {response.grounding_metadata}")



grounding(project_id=config.PROJECT_ID, location='us-central1', data_store_location='global', data_store_id='quarterly-reports')
