from typing import Optional

from pydantic import BaseModel
from datetime  import datetime

class CategoryRequestDto(BaseModel):
    name:str
    description:Optional[str] = None

class CategoryResponseDto(BaseModel):
    id: str
    description: str
    created_at: datetime
    updated_at: datetime