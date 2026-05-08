from .providers import QdrantDB
from .vectorDBEnums import vectorDBEnums
from controllers import BaseController
class VectorDBProviderFactory():
    def __init__(self , config):
        self.config = config
        self.base_controller = BaseController()
    
    def create(self , provider: str):
        if provider == vectorDBEnums.QDRANT.value: 
            db_path = self.base_controller.get_database_path(db_name = self.config.VECTOR_DB_PATH)
            return QdarntDB(
                db_path = db_path , 
                distance_method = self.config.VECTOR_DISTANCE_METHOD
            )
