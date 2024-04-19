from requests.exceptions import RequestException
from src.config.logging import logger
from src.config.setup import config
from typing import Dict
from typing import Any
import requests
import json


LOCATION = 'us-central1'
endpoint = f"https://{LOCATION}-prediction-aiplatform.googleapis.com/v1beta1/projects/{config.PROJECT_ID}/locations/{LOCATION}/publishers/google/models/{config.TEXT_GEN_MODEL_NAME}:generateContent"
   
# Headers for the request
headers = {
    "Authorization": f"Bearer {config.ACCESS_TOKEN}",
    "Content-Type": "application/json; charset=utf-8",
    
}
prompt = 'Who was the chief minister of Tamil Nadu in 1986?'

payload = {
    "contents": [{
        "parts": [{
            "text": "prompt"
        }]
    }],
    "tools": {  
        "googleSearchRetrieval": {}
    },
    "model": config.TEXT_GEN_MODEL_NAME,
    
}


print(endpoint)
print(headers)
print(payload)


response = requests.post(endpoint, headers=headers, json=payload, stream=False)
print(response.content)
    

