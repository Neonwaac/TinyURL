from src.database.mongo_connection import get_mongo_client
from datetime import datetime

class MetadataModel:
    @staticmethod
    def create_metadata(codigo, imagen=None, descripcion=None):
        db = get_mongo_client()
        metadata = {
            "_id": codigo,
            "imagen": imagen,
            "descripcion": descripcion,
            "createdAt": datetime.utcnow()
        }
        try:
            db.links_metadata.insert_one(metadata)
            return True
        except Exception as e:
            print(f"Error creating metadata: {e}")
            return False

    @staticmethod
    def get_metadata(codigo):
        db = get_mongo_client()
        try:
            metadata = db.links_metadata.find_one({"_id": codigo})
            return metadata
        except Exception as e:
            print(f"Error getting metadata: {e}")
            return None
