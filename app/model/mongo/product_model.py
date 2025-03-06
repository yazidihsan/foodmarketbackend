from typing import Optional

from bson import ObjectId
from fastapi.encoders import ENCODERS_BY_TYPE
from pydantic import Field, BaseModel
from datetime import datetime

from app.model.mongo.common_model import PyObjectId


class ProductModel(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    name: str
    description: Optional[str] = None
    price : float
    category_id : str
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

    class Config:
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True
        populate_by_name = True
        allow_population_by_field_name = True

    def model_dump(self, *args, **kwargs):
        """Override model_dump to handle ObjectId and Enum serialization"""
        kwargs["by_alias"] = True
        data = super().model_dump(*args, **kwargs)
        # Convert enum to string for MongoDB
        if "status" in data:
            data["status"] = str(data["status"])
        return data