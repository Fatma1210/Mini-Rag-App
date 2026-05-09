from fastapi import FastAPI
from routes import base , data
from motor.motor_asyncio import AsyncIOMotorClient

from helpers.config import Settings , get_settings 

from store.llms.LLMSProviderFactory import LLMSProviderFactory

from store.vectordb.VectorDBProviderFactory import VectorDBProviderFactory
app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    settings = get_settings()

    app.mongodb_conn = AsyncIOMotorClient(settings.MONGODB_URI)
    app.db_client = app.mongodb_conn[settings.MONGODB_DATABASE]

    llm_provider_factory = LLMSProviderFactory(settings)
    vectordb_provider_factory = VectorDBProviderFactory(settings)
    
    #Generation_Client
    app.generation_client = llm_provider_factory.create(provider = settings.GENERATION_BACKEND)
    app.generation_client.set_generation_model(model_id = settings.GENERATION_MODEL_ID)

    #Embedding_Client
    app.embedding_client = llm_provider_factory.create(provider = settings.EMBEDDING_BACKEND)
    app.embedding_client.set_embedding_model(
        model_id = settings.EMBEDDING_MODEL_ID , 
        embedding_size = settings.EMBEDDING_MODEL_SIZE
        )

    #Vector_DataBase_Client
    app.vector_vectordb_client = vectordb_provider_factory.create(
        provider = settings.VECTOR_DB_BACKEND
    )

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_conn.close() 

app.include_router(base.base_router)
app.include_router(data.data_router)