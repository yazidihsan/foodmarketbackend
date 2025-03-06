from typing import List

from fastapi import APIRouter,HTTPException

from app.constant.messages import SuccessMessages
from app.dto.product_dto import  ProductRequestDto
from app.model.mongo.product_model import  ProductModel
from app.service.product_service import  ProductService
from app.validation.product_validation import validate_product_data

router = APIRouter(prefix="/product",tags=["Product"])


@router.post("/create")
async def create_product(product_data:ProductRequestDto):

    try:
        # validate_data = validate_product_data(product_data)
        product_service = ProductService()
        product = await product_service.create_product(product_data.model_dump())

        return {"message": SuccessMessages.PRODUCT_CREATED,"product": product}


    except ValueError as e :
        raise HTTPException(status_code=400,detail=str(e))

@router.get("/{product_id}")
async def get_product_by_id(product_id:str):

    try:

        product_service = ProductService()
        product_data:ProductModel = await product_service.get_product_by_id(product_id)

        return {"message": SuccessMessages.GET_CATEGORY_BY_ID,"product":product_data}

    except ValueError as e :
        raise HTTPException(status_code=400,detail=e)

@router.get("")
async def get_all_products():

    try:
        product_service = ProductService()
        products:List[ProductModel] = await product_service.get_all_products()

        return {"message": SuccessMessages.GET_ALL_PRODUCTS,"products":products}

    except ValueError as e :
        raise HTTPException(status_code=400, detail=e)

@router.put("/{product_id}")
async def update_product(product_id:str,input_data:ProductRequestDto):

    try:
        product_service = ProductService()
        product_data = await product_service.update_product(product_id, input_data)

        return {"message": SuccessMessages.PRODUCT_UPDATED,"product":product_data}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=e)

@router.delete("/{product_id}")
async def delete_product(product_id:str):

    try:
        product_service = ProductService()
        await product_service.delete_product(product_id)

        return {"message": SuccessMessages.PRODUCT_DELETED}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=e)





