from bson import ObjectId
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.synchronous.database import Database

from app.config.settings import settings
from app.dto.user_dto import UserRegistrationDto
from app.model.mongo.user_model import UserModel


class UserRepository:
   def __init__(self):
       self.client = AsyncIOMotorClient(settings.MONGODB_URL)
       self.db = self.client[settings.DATABASE_NAME]
       self.repository = self.db.users

   def insert_new_user(self,input_data:UserModel):
       return self.repository.insert_one(input_data)

   def get_user_by_id(self,user_id:str):

       result = self.repository.find_one({"_id": ObjectId(user_id)})

       if result is None :
           return None

       return result

   def find_user_by_username(self, email: str):
       result = self.repository.find_one({"email": email})

       if result is not None:
           return result

       return None


userRepository = UserRepository()
