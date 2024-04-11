from langchain.prompts.chat import HumanMessagePromptTemplate, ChatPromptTemplate
from langchain_google_vertexai import ChatVertexAI
from src.config.logging import logger
from src.config.setup import config
from typing import Optional


class LLM:
    """
    A class representing a Language Model using Vertex AI.

    Attributes:
        model (ChatVertexAI): The chat model loaded from Vertex AI.
    """

    def __init__(self) -> None:
        """
        Initializes the LLM class by loading the chat model.
        """
        self.model = self._initialize_model()

    def _initialize_model(self) -> Optional[ChatVertexAI]:
        """
        Loads the chat model from Vertex AI.

        Returns:
            ChatVertexAI: An instance of the Vertex AI chat model.
        """
        try:
            model = ChatVertexAI(
                model_name=config.TEXT_GEN_MODEL_NAME,
                temperature=0.0,
                max_output_tokens=1024,
                verbose=True
            )
            logger.info("Chat model loaded successfully.")
            return model
        except Exception as e:
            logger.error(f"Failed to load the model: {e}")
            return None

    def predict(self, task: str, query: str) -> Optional[str]:
        """
        Generates a response for a given task and query using the chat model.

        Args:
            task (str): The task to be performed by the model.
            query (str): The query or input text for the model.

        Returns:
            Optional[str]: The model's response or None if an error occurred.
        """
        try:
            human_template = "{task}\nQuery:\n{query}"
            human_message = HumanMessagePromptTemplate.from_template(human_template)
            chat_template = ChatPromptTemplate.from_messages([human_message])
            prompt = chat_template.format_prompt(task=task, query=query).to_messages()
            response = self.model.invoke(prompt)
            completion = response.content
            return completion
        except Exception as e:
            logger.error(f"Error during model prediction: {e}")
            return None