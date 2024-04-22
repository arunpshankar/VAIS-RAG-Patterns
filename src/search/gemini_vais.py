from vertexai.preview.generative_models import GenerationResponse
from vertexai.preview.generative_models import GenerationConfig
from vertexai.preview.generative_models import GenerativeModel
from vertexai.preview.generative_models import grounding
from vertexai.preview.generative_models import Tool
from src.config.logging import logger
from src.config.setup import config
from typing import Optional


# Constants
MODEL_NAME = 'gemini-1.0-pro-002'
TEMPERATURE = 0.0  # Gemini Pro 002 temperature can be set between 0 and 2
MAX_OUTPUT_TOKENS = 8192
TOP_P = 0.0  # TOP_K is not applicable to Gemini Pro 002
DATA_STORE_LOCATION = 'global'


def generate_text_with_grounding_vais(data_store_path: str, query: str) -> Optional[GenerationResponse]:
    """
    Generates text using the Gemini model with grounding based on Vertex AI Search (Agent Builder).
    
    Parameters:
        data_store_path (str): Path to the data store used for retrieval.
        query (str): The input text prompt for generating the response.
        
    Returns:
        Optional[GenerationResponse]: The generated response object if successful, None otherwise.
    """
    try:
        # Load the model
        model = GenerativeModel(model_name=MODEL_NAME)

        # Set up Vertex AI Search as the retrieval tool
        tool = Tool.from_retrieval(grounding.Retrieval(grounding.VertexAISearch(datastore=data_store_path)))

        # Generate response with specified configurations
        response = model.generate_content(
            query,
            tools=[tool],
            generation_config=GenerationConfig(
                temperature=TEMPERATURE,
                max_output_tokens=MAX_OUTPUT_TOKENS,
                top_p=TOP_P
            )
        )
        return response
    except Exception as e:
        logger.error(f"Error during text generation: {e}", exc_info=True)
        return None


def extract_answer_from_response(response: Optional[GenerationResponse]) -> Optional[str]:
    """
    Extracts the text part of the answer from the response object.
    
    Parameters:
        response (Optional[GenerationResponse]): The response object from which to extract the text.
        
    Returns:
        Optional[str]: The extracted text if the response contains any, None otherwise.
    """
    if response is None or not response.candidates:
        return None
    return response.candidates[0].content.parts[0].text


if __name__ == '__main__':
    data_store_id = 'quarterly-reports'
    data_store_path = f'projects/{config.PROJECT_ID}/locations/{DATA_STORE_LOCATION}/collections/default_collection/dataStores/{data_store_id}'
    query = "How much did Amazon's net sales increase in Q2 2021 compared to Q2 2020?"

    response = generate_text_with_grounding_vais(data_store_path, query)
    print(response)
    if response:
        answer = extract_answer_from_response(response)
        print(f"Generated answer: {answer}")
    else:
        print("Failed to generate response.")