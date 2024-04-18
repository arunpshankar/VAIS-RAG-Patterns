from vertexai.preview.generative_models import GenerativeModel
from vertexai.preview.generative_models import grounding
from vertexai.preview.generative_models import Tool
from src.config.logging import logger 
from src.config.setup import config



# model = GenerativeModel(config.TEXT_GEN_MODEL_NAME)
model = GenerativeModel('gemini-1.0-pro')

ENGINE_ID = "quarterly-reports"
LOCATION = "global"

data_store = f"projects/{config.PROJECT_ID}/locations/{LOCATION}/collections/default_collection/dataStores/{ENGINE_ID}"


tool = Tool.from_retrieval(grounding.Retrieval(grounding.VertexAISearch(datastore=data_store)))

question = "What was the year-over-year percentage change in revenue from Xbox content and services for the three months ended March 31, 2023, both in GAAP and constant currency terms?"
response = model.generate_content(question, tools=[tool])

answers = response.candidates
print(answers)




if __name__ == '_-main__':
    pass