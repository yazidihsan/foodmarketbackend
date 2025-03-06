from typing import  Optional

from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from app.enums.user_status import UserStatus
from app.model.mongo.common_model import PyObjectId


class UserModel(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    # id: PyObjectId = Field(alias="_id")
    email: EmailStr
    password: str
    full_name: str
    status: UserStatus = UserStatus.ACTIVE
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

