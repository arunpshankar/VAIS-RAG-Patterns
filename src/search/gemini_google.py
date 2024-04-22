from vertexai.preview.generative_models import GenerationResponse
from vertexai.preview.generative_models import GenerationConfig
from vertexai.preview.generative_models import GenerativeModel
from vertexai.preview.generative_models import grounding 
from vertexai.preview.generative_models import Tool
from src.config.logging import logger 
from src.config.setup import *
from typing import Optional
from typing import Tuple
from typing import List 


# Constants
MODEL_NAME = 'gemini-1.0-pro-002'
TEMPERATURE = 0.0  # Gemini temperature can be set between 0 and 2
MAX_OUTPUT_TOKENS = 8192
TOP_P = 0.0  # TOP_K is not applicable to Gemini pro 002


def generate_text_with_grounding_web(prompt: str) -> Optional[str]:
    """
    Generates text using the Gemini model with grounding based on Google Search.
    
    Parameters:
        prompt (str): The input text prompt for generating the response.
        
    Returns:
        Optional[str]: The generated text if successful, None otherwise.
    """
    try:
        # Load the model
        model = GenerativeModel(model_name=MODEL_NAME)

        # Use Google Search for grounding
        tool = Tool.from_google_search_retrieval(grounding.GoogleSearchRetrieval())

        # Generate response with specified configurations
        response = model.generate_content(
            prompt,
            tools=[tool],
            generation_config=GenerationConfig(
                temperature=TEMPERATURE,
                max_output_tokens=MAX_OUTPUT_TOKENS,
                top_p=TOP_P
            ),
        )
        answer = response.candidates[0].content.parts[0].text
        return answer
    except Exception as e:
        logger.error(f"Error during text generation: {e}", exc_info=True)
        return None
    

if __name__ == '__main__':
    query = "How much did Amazon's net sales increase in Q2 2021 compared to Q2 2020?"
    response = generate_text_with_grounding_web(query)
    if response is not None:
        print(response)
    else:
        print("Failed to generate response.")