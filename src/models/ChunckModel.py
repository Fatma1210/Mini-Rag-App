from .BaseDataModel import BaseDataModel
from .db_schemes import DataChunk
from .enums.DataBaseEnumerations import DataBaseEnum
from bson import ObjectId
from pymongo import InsertOne
class ChunckModel(BaseDataModel):
    def __init__(self , db_client: object):
        super().__init__(db_client= db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_CHUNK_NAME.value]

    async def init_collection(self):
        all_collections = await self.db_client.list_collection_names()
        if DataBaseEnum.COLLECTION_CHUNK_NAME.value not in all_collections:
            await self.db_client.create_collection(DataBaseEnum.COLLECTION_CHUNK_NAME.value)
            #create indexes for the collection
            indexes = DataChunk.get_indexes()
            for index in indexes:
                await self.collection.create_index(
                    index["key"] ,
                     name= index["name"] , unique= index["unique"]
                    )
    @classmethod
    async def create_instance(cls , db_client: object):
        instance = cls(db_client= db_client)
        await instance.init_collection()
        return instance

    def create_chunk(self , chunk: DataChunk):
        result = self.collection.insert_one(chunk.dict(by_alias=True , exclude_unset=True))
        chunk.id = result.inserted_id

        return chunk

    def get_chunk(self , chunk_id: str):
        record =  self.collection.find_one((
            {"_id": ObjectId(chunk_id)}
        ))
        if record is None: 
            return None
        return DataChunk(**record)
    
    async def get_all_chunks(self , page: int = 1 , page_size: int = 10):
        
        #count total number of chunks in the collection
        total_chunks = await self.collection.count_documents({})

        #calculate total number of pages
        total_pages = (total_chunks + page_size - 1) // page_size

        cursor = self.collection.find().skip((page - 1) * page_size).limit(page_size)
        
        chunks = []
        async for document in cursor:
            chunks.append(chunk(**document))

        return chunks , total_pages
    
    async def insert_many_chunks(self, chunks: list, batch_size: int = 100):
        try:
            print(f">>> total chunks to insert: {len(chunks)}")
            print(f">>> collection: {self.collection.name}")
            print(f">>> sample chunk: {chunks[0].model_dump() if chunks else 'EMPTY'}")
            
            for i in range(0, len(chunks), batch_size):
                batch = chunks[i:i + batch_size]
                operations = [InsertOne(chunk.model_dump()) for chunk in batch]
                result = await self.collection.bulk_write(operations)
                print(f">>> batch {i} inserted: {result.inserted_count}")
            
            return len(chunks)
        except Exception as e:
            print(f">>> insert error: {e}")
            return 0


    async def delete_chunks_by_project_id(self , project_id: str):
        result = await self.collection.delete_many(
            {"chunk_project_id": project_id}
        )
        return result.deleted_count