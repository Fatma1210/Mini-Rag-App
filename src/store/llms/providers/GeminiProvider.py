from ..LLMInterface import LLMInterface
from google import genai
from google.genai import types
from ..LLMEnums import GeminiEnums
import logging



class GeminiProvider(LLMInterface):
    
    def __init__(self , api_key: str ,
                         default_input_max_characters: int = 1000 ,
                         default_output_max_tokens: int = 1000 ,
                         default_temperature: float = 0.1):
        self.api_key = api_key
    
        self.default_input_max_characters = default_input_max_characters
        self.default_output_max_tokens = default_output_max_tokens
        self.default_temperature = default_temperature

        self.generation_model_id = None

        self.embedding_model_id = None
        self.embedding_size = None

        self.enums = GeminiEnums

        self.client = genai.Client(api_key=self.api_key)

        self.logger = logging.getLogger(__name__)
        

    def set_generation_model(self , model_id: str):
        self.generation_model_id = model_id
        

    def set_embedding_model(self , model_id: str , embedding_size: int):
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size
    
    def process_text(self , text: str):
        return text[:self.default_input_max_characters].strip()

    def generate_text(self, prompt: str, chat_history: list = [], max_output_tokens: int = None, temperature: float = None):
        if self.client is None:
            self.logger.error("Gemini client not initialized.")
            return None
        if self.generation_model_id is None:
            self.logger.error("Generation model not set.")
            return None

        max_output_tokens = max_output_tokens if max_output_tokens else self.default_output_max_tokens
        temperature = temperature if temperature else self.default_temperature

        system_instruction = None
        conversation = []

        for msg in chat_history:
            if msg["role"] == "system":
                system_instruction = msg["parts"][0]["text"]
            else:
                conversation.append(
                    msg["parts"][0]["text"]
                )

        conversation.append(self.construct_prompt(prompt, GeminiEnums.USER.value))

        response = self.client.models.generate_content(
            model=self.generation_model_id,
            contents=conversation,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=temperature,
                max_output_tokens=max_output_tokens
            )
        )

        if response is None or not response.text:
            self.logger.error("Error while generating text with Gemini.")
            return None

        return response.text
    def generate_embeddings(self , text: str , document_type: str = None):
        if not self.client:
          self.logger.error("Gemini client not initialized.")
          return None
        if not self.embedding_model_id:
          self.logger.error("Embedding model not set.")
          return None
        response = self.client.models.embed_content(
                model=  self.embedding_model_id,
                contents=text,
                config=types.EmbedContentConfig(output_dimensionality=10),
            )
        if response is None or not response.data or len(response.data) == 0 or response.data[0].embedding is None:
            self.logger.error("No embedding returned from Gemini.")
            return None
        return response.embeddings[0].values

    def construct_prompt(self , prompt: str , role: str):
        return {
                "role": role,
                "parts": [{"text": prompt}]
            }