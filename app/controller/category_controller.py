from typing import List

from fastapi import APIRouter,HTTPException

from app.constant.messages import SuccessMessages
from app.dto.category_dto import CategoryRequestDto
from app.model.mongo.category_model import CategoryModel
from app.service.category_service import CategoryService
from app.validation.category_validation import validate_category_data

router = APIRouter(prefix="/category",tags=["Category Product"])


@router.post("/create")
async def create_category(category_data:CategoryRequestDto):

    try:
        validate_data = validate_category_data(category_data)
        category_service = CategoryService()
        category = await category_service.create_category(validate_data.model_dump())

        return {"message": SuccessMessages.CATEGORY_CREATED,"category": category}


    except ValueError as e :
        raise HTTPException(status_code=400,detail=str(e))

@router.get("/{category_id}")
async def get_category_by_id(category_id:str):

    try:

        category_service = CategoryService()
        category_data:CategoryModel = await category_service.get_category_by_id(category_id)

        return {"message": SuccessMessages.GET_CATEGORY_BY_ID,"category":category_data}

    except ValueError as e :
        raise HTTPException(status_code=400,detail=e)

@router.get("")
async def get_all_categories():

    try:
        category_service = CategoryService()
        categories:List[CategoryModel] = await category_service.get_all_categories()

        return {"message": SuccessMessages.GET_ALL_CATEGORIES,"categories":categories}

    except ValueError as e :
        raise HTTPException(status_code=400, detail=e)

@router.put("/{category_id}")
async def update_category(category_id:str,input_data:CategoryRequestDto):

    try:
        category_service = CategoryService()
        category_data = await category_service.update_category(category_id, input_data)

        return {"message": SuccessMessages.CATEGORY_UPDATED,"category":category_data}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=e)

@router.delete("/{category_id}")
async def delete_category(category_id:str):

    try:
        category_service = CategoryService()
        await category_service.delete_category(category_id)

        return {"message": SuccessMessages.CATEGORY_DELETED}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=e)





