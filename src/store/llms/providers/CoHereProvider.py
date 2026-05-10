from ..LLMInterface import LLMInterface
from ..LLMEnums import CoHereEnums , DocumentTypesEnums
import logging
import cohere
class CoHereProvider(LLMInterface):
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

        self.client = cohere.ClientV2(
            api_key=self.api_key 
        )

        self.logger = logging.getLogger(__name__)

        
    def set_generation_model(self , model_id: str):
        self.generation_model_id = model_id
        

    def set_embedding_model(self , model_id: str , embedding_size: int):
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size
    
    def process_text(self , text: str):
        return text[:self.default_input_max_characters].strip()
    
    def generate_text(self , prompt: str , chat_history: list = [] ,
     max_output_tokens: int = None , temperature: float = None):
        if self.client is None:
            self.logger.error("CoHere client not initialized.")
            return None
        if self.generation_model_id is None:
            self.logger.error("Generation model not set.")
            return None
        max_output_tokens = max_output_tokens if max_output_tokens else self.default_output_max_tokens
        temperature = temperature if temperature else self.default_temperature
        
        
        response = self.client.chat(
            model=self.generation_model_id,
            chat_history=chat_history , 
            message=self.process_text(prompt) ,
            max_tokens=max_output_tokens,
            temperature=temperature

        )
        if response and response.text:
            chat_history.append(self.construct_prompt(prompt , CoHereEnums.USER.value))
            return response.text.strip()
        else:
            self.logger.error("No response text received from CoHere.")
            return None

    def generate_embeddings(self , text: str ,document_type: str = None ):
        if self.client is None:
            self.logger.error("CoHere client not initialized.")
            return None
        if self.embedding_model_id is None:
            self.logger.error("Embedding model not set.")
            return None
        input_type = CoHereEnums.DOCUMENT
        if document_type == DocumentTypesEnums.QUERY.value:
            input_type = CoHereEnums.QUERY
        else :
            input_type = CoHereEnums.DOCUMENT
        response = self.client.embed(
            model=self.embedding_model_id,
            texts=[text],
            input_type=input_type.value,
            embedding_types=['float']
        )
        if response and response.embeddings and response.embeddings.float:
            return response.embeddings.float[0]
        else:
            self.logger.error("No embeddings received from CoHere.")
            return None
    def construct_prompt(self , prompt: str , role: str):
        return {
            "role": role,
            "text": self.process_text(prompt)
        }