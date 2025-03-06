from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

from app.config.settings import settings
from app.dto.product_dto import ProductRequestDto
from app.model.mongo.product_model import ProductModel


class ProductRepository:
    def __init__(self):
        self.client = AsyncIOMotorClient(settings.MONGODB_URL)
        self.db = self.client[settings.DATABASE_NAME]
        self.repository = self.db.products

    async def insert_new_product(self,input_data:ProductModel):
            return await self.repository.insert_one(input_data)

    async def find_by_product_name(self,name:str):
            result = await self.repository.find_one({"name":name})

            if result is not None:
                return result

            return None

    async def get_product_by_id(self,product_id:str):
            result = await self.repository.find_one({"_id":ObjectId(product_id)})

            if result is None:
                return None

            return result

    async def get_all_products(self):
            products = await self.repository.find().to_list(length=None)
            return [ProductModel(**product) for product in products]


    async def update_product(self,product_id:str,input_data:ProductRequestDto):
            return await self.repository.update_one(
                {"_id": ObjectId(product_id)},
                {"$set":input_data.model_dump(exclude_unset=True)},
                upsert=True)

    async def delete_product(self,product_id:str):
            await self.repository.delete_one({"_id":ObjectId(product_id)})

productRepository = ProductRepository()