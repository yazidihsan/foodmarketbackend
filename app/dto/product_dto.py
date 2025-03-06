from typing import Optional

from pydantic import BaseModel


class ProductRequestDto(BaseModel):
    name:str
    description:Optional[str] = None
    price:float
    category_id: str


class ProductResponseDto(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    price: float
    categoryId: str