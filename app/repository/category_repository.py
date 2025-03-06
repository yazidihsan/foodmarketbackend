from typing import List

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

from app.config.settings import settings
from app.dto.category_dto import CategoryRequestDto
from app.model.mongo.category_model import  CategoryModel


class CategoryRepository:
    def __init__(self):
        self.client = AsyncIOMotorClient(settings.MONGODB_URL)
        self.db = self.client[settings.DATABASE_NAME]
        self.repository = self.db.categories

    async def insert_new_category(self,input_data:CategoryModel):
        return await self.repository.insert_one(input_data)

    async def find_by_category_name(self,name:str):
        result = await self.repository.find_one({"name":name})

        if result is not None:
            return result

        return None

    async def get_category_by_id(self,category_id:str):
        result = await self.repository.find_one({"_id":ObjectId(category_id)})

        if result is None:
            return None

        return result

    async def get_all_category(self):
        categories = await self.repository.find().to_list(length=None)
        return [CategoryModel(**category) for category in categories]
        # return categories

    async def update_category(self,category_id:str,input_data:CategoryRequestDto):
        return await self.repository.update_one(
            {"_id": ObjectId(category_id)},
            {"$set":input_data.model_dump(exclude_unset=True)},
            upsert=True)

    async def delete_category(self,category_id:str):
        await self.repository.delete_one({"_id":ObjectId(category_id)})

categoryRepository = CategoryRepository()


