from typing import List

from app.constant.messages import ErrorMessages
from app.dto.category_dto import CategoryRequestDto

from app.model.mongo.category_model import  CategoryModel

from app.repository.category_repository import categoryRepository


class CategoryService:
    def __init__(self):
        self.category_repository = categoryRepository

    async def create_category(self,category_data:dict)->CategoryModel:


        existing_category =await self.category_repository.find_by_category_name(category_data["name"])

        if existing_category :
            raise ValueError(ErrorMessages.CATEGORY_EXISTS)

        category_product = CategoryModel(**category_data)

        category_dict = category_product.model_dump(exclude={"_id"})
        result = await self.category_repository.insert_new_category(category_dict)
        category_product.id = result.inserted_id


        return category_product


    async def get_category_by_id(self,category_id:str)->CategoryModel:
        category_product = await self.category_repository.get_category_by_id(category_id)

        if category_product is None:
            raise ValueError(ErrorMessages.CATEGORY_NOT_FOUND)

        category_data = CategoryModel(**category_product)

        return category_data

    async def get_all_categories(self)->List[CategoryModel]:
        categories = []
        category_products = await self.category_repository.get_all_category()

        for category in category_products :
            categories.append(category)

        return categories

    async def update_category(self,category_id:str, category_data:CategoryRequestDto)->CategoryModel:
        existing_category = await self.get_category_by_id(category_id)

        if existing_category is None:
            raise ValueError(ErrorMessages.CATEGORY_NOT_FOUND)

        if existing_category.name is not None:
            existing_category.name = category_data.name
        else:
            existing_category.name = None
        if existing_category.description is not None:
            existing_category.description = category_data.description
        else:
            existing_category.description = None

        await self.category_repository.update_category(
           category_id,existing_category
        )

        return existing_category


    async def delete_category(self,category_id:str):
        await self.category_repository.delete_category(category_id)




