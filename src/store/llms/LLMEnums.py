from enum import Enum

class LLMEnums(Enum):
    OPENAI = "OPENAI"
    COHERE = "COHERE"
    ANTHROPIC = "ANTHROPIC"
    AZURE_OPENAI = "AZURE_OPENAI"
    CUSTOM = "CUSTOM"

class OpenAIEnums(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"