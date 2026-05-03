from fastapi import FastAPI , UploadFile , Depends , APIRouter , status
from fastapi.responses import JSONResponse
from helpers.config import Settings , get_settings
from controllers import DataController , ProjectController , ProcessController
from models import ResponseSignal
import aiofiles
import os
import logging
from .schemes.data import ProcessRequest

logger = logging.getLogger("uvicorn.error")
data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1 , data"],
)


@data_router.post("/upload/{project_id}")
async def upload_file(project_id: str , file: UploadFile , 
                                         app_settings: Settings = Depends(get_settings)):
   
    
                    data_controller = DataController()
                    #validate file properties -> logic : controller
                    
                    is_valid, result_signal = data_controller.validate_uploaded_file(file=file)

                    if not is_valid:
                        return JSONResponse(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            content={
                                "signal": result_signal
                            }
                        ) 
                    project_dir_path = ProjectController().get_project_path(project_id=project_id)
                    file_location , file_id = data_controller.generate_unique_file_path(
                        orig_file_name=file.filename,
                        project_id=project_id
                    )
                    try:
                        async with aiofiles.open(file_location , "wb") as f:
                            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE): # read file in chunks
                                await f.write(chunk)
                    except Exception as e:
                        loggor.error(f"Error while Uploading file: {e}")

                        return JSONResponse(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            content={
                                "signal": ResponseSignal.FILE_UPLOAD_FAILED.value
                            }
                        )
                    return JSONResponse(
                        status_code=status.HTTP_200_OK,
                        content={
                            "signal": ResponseSignal.FILE_UPLOAD_SUCCESS.value,
                            "file_id": file_id
                        }   
                        
                        )


@data_router.post("/process/{project_id}")
async def process_file(project_id: str , request: ProcessRequest):
    
    file_id = request.file_id
    chunk_size = request.chunk_size
    overlap_size = request.overlap_size


    process_controller = ProcessController(project_id=project_id)

    file_content = process_controller.get_file_content(file_id=file_id)

    file_chunks = process_controller.process_file_content(
        file_content=file_content,
        file_id=file_id,
        chunnk_size=chunk_size,
        overlap_size=overlap_size
        )
    if file_chunks is None or len(file_chunks) == 0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignal.FILE_PROCESSING_FAILED.value
            }
        )
    return file_chunks
    # return JSONResponse(
    #     status_code=status.HTTP_200_OK,
    #     content={
    #         "signal": ResponseSignal.FILE_PROCESSING_SUCCESS.value,
    #         "chunks": len(file_chunks) ,
        
    #     }
    # )