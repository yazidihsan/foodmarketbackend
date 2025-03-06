
from typing import List

from app.constant.messages import ErrorMessages
from app.dto.product_dto import ProductRequestDto

from app.model.mongo.product_model import  ProductModel
from app.repository.category_repository import categoryRepository

from app.repository.product_repository import productRepository


class ProductService:
    def __init__(self):
        self.product_repository = productRepository
        self.category_repository = categoryRepository

    async def create_product(self,product_data:dict)->ProductModel:

        category = await self.category_repository.get_category_by_id(product_data['category_id'])  # Use 'category_id'

        exist_product = await self.product_repository.find_by_product_name(product_data["name"])

        if exist_product:
            raise ValueError(ErrorMessages.PRODUCT_EXISTS)

        if not category:
            raise ValueError(ErrorMessages.CATEGORY_NOT_FOUND)

        product = ProductModel(**product_data)

        product_dict = product.model_dump(exclude={"_id"})
        result = await self.product_repository.insert_new_product(product_dict)
        product.id = result.inserted_id

        return product


    async def get_product_by_id(self,product_id:str)->ProductModel:
        product_product = await self.product_repository.get_product_by_id(product_id)

        if product_product is None:
            raise ValueError(ErrorMessages.PRODUCT_NOT_FOUND)

        product_data = ProductModel(**product_product)

        return product_data

    async def get_all_products(self)->List[ProductModel]:
        categories = []
        product_products = await self.product_repository.get_all_products()

        for product in product_products :
            categories.append(product)

        return categories

    async def update_product(self,product_id:str, product_data:ProductRequestDto)->ProductModel:
        existing_product = await self.get_product_by_id(product_id)

        if existing_product is None:
            raise ValueError(ErrorMessages.PRODUCT_NOT_FOUND)

        if existing_product.name is not None:
            existing_product.name = product_data.name
        else:
            existing_product.name = None
        if existing_product.description is not None:
            existing_product.description = product_data.description
        else:
            existing_product.description = None

        await self.product_repository.update_product(
           product_id,existing_product
        )



        return existing_product


    async def delete_product(self,product_id:str):
        await self.product_repository.delete_product(product_id)




