from fastapi import FastAPI , UploadFile , Depends , APIRouter , status
from fastapi.responses import JSONResponse
from helpers.config import Settings , get_settings
from controllers import DataController

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
                    else:
                        return JSONResponse(
                            status_code=status.HTTP_200_OK,
                            content={
                                "signal": result_signal
                            }
                        )