from .BaseController import BaseController

from .ProjectController import ProjectController

from langchain_community.document_loaders import PyMuPDFLoader, TextLoader

from langchain.text_splitter import RecursiveCharacterTextSplitter

from models import ProcessingEnum

import os
class ProcessController(BaseController):
    def __init__(self , project_id: str):
        super().__init__()

        self.project_id = project_id
        self.project_path = ProjectController().get_project_path(project_id = project_id)

    def get_file_extension(self , file_name: str):
        return os.path.splitext(file_name)[1].lower()


    def get_file_loader(self , file_id: str):
        file_ext = self.get_file_extension(file_id)
        file_path = os.path.join(self.project_path , file_id)
        if file_ext == ProcessingEnum.TXT.value:
            return TextLoader(file_path , encoding="utf-8")

        if file_ext == ProcessingEnum.PDF.value:
            return PyMuPDFLoader(file_path)

        return None
    
    def get_file_content(self , file_id: str):
        loader = self.get_file_loader(file_id=file_id)
        if loader is None:
            return None
        return loader.load() # returns list of documents with page content and metadata (page number)


    def process_file_content(self , file_content: list , file_id: str , 
                                   chunnk_size: int = 100 , overlap_size: int = 20):
            text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunnk_size , 
            chunk_overlap=overlap_size,
            length_function = len,
            )   

            file_content_texts = [
                rec.page_content
                for rec in file_content
            ]
            file_content_metadata = [
                rec.metadata
                for rec in file_content
            ]

            chunks = text_splitter.create_documents(
                file_content_texts , 
                metadatas=file_content_metadata
                )
            return chunks