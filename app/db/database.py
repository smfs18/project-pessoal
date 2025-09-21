import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

class MongoManager:
    def __init__(self):
        self.mongo_uri = os.getenv("MONGO_URI")
        self.db_name = os.getenv("DB_NAME")
        if not self.mongo_uri or not self.db_name:
            raise ValueError("MONGO_URI e DB_NAME devem ser definidos no arquivo .env")
        
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.db_name]
        self.conversations = self.db.conversations

# Instância única para ser usada em toda a aplicação
db_manager = MongoManager()

def get_database():
    return db_manager.conversations