from ..LLMInterface import LLMInterface
from ..LLMEnums import GroqEnums , DocumentTypesEnums
import logging
import os
from groq import Groq




class GroqProvider(LLMInterface):
    
    def __init__(self , api_key: str , api_url: str = None ,
                        default_input_max_characters: int = 10000 ,
                         default_output_max_tokens: int = 10000 ,
                         default_temperature: float = 0.1):
        self.api_key = api_key
        self.api_url = api_url
    
        self.default_input_max_characters = default_input_max_characters
        self.default_output_max_tokens = default_output_max_tokens
        self.default_temperature = default_temperature

        self.generation_model_id = None

   

        self.enums = GroqEnums

        self.client = Groq(
            api_key=self.api_key ,
            base_url=self.api_url
        )

        self.logger = logging.getLogger(__name__)
        

    def set_generation_model(self , model_id: str):
        self.generation_model_id = model_id
        

    def set_embedding_model(self , model_id: str , embedding_size: int):
        pass
    
    def process_text(self , text: str):
        return text[:self.default_input_max_characters].strip()

    def generate_text(self , prompt: str , chat_history: list = [] , max_output_tokens: int = None , temperature: float = None):
        if self.client is None:
            self.logger.error("Groq client not initialized.")
            return None
        if self.generation_model_id is None:
            self.logger.error("Generation model not set.")
            return None
        max_output_tokens = max_output_tokens if max_output_tokens else self.default_output_max_tokens
        temperature = temperature if temperature else self.default_temperature
        
        chat_history.append(self.construct_prompt(prompt , GroqEnums.USER.value))
        
        response = self.client.chat.completions.create(
            model=self.generation_model_id,
            messages=chat_history,
            max_tokens=max_output_tokens,
            temperature=temperature
        )
        if response is None or not response.choices or len(response.choices) == 0 or not response.choices[0].message or not response.choices[0].message.content:
            self.logger.error("Error while generation text with Groq.")
            return None

        return response.choices[0].message.content.strip()
         
    def generate_embeddings(self , text: str , document_type: str = None):
        pass



    def construct_prompt(self , prompt: str , role: str):
        return {
            "role": role,
            "content": prompt
        }