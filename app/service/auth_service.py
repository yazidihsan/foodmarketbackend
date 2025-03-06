from typing import Optional

from bson import ObjectId
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

from app.config.settings import  settings
from app.constant.messages import ErrorMessages
from app.dto.user_dto import UserResponseDto
from app.enums.user_status import UserStatus
from app.model.mongo.user_model import UserModel
from app.repository.user_repository import userRepository
from app.utils.password_utils import hash_password, verify_password


class AuthService:
    def __init__(self):
        self.user_repository = userRepository
        # print(f"DEBUG INIT: {settings.MONGODB_URL}")
        # self.client = AsyncIOMotorClient(settings.MONGODB_URL)
        # self.db = self.client[settings.DATABASE_NAME]
        # self.collection = self.db.users

    async def create_user(self,user_data:dict)->UserModel:
        existing_user = await self.user_repository.find_user_by_username(user_data["email"])
        if existing_user:
            raise ValueError(ErrorMessages.USER_EXISTS)
        user_data["password"] = hash_password(user_data["password"])
        user = UserModel(**user_data)

        # # Convert to dict and ensure enum is serialized as string
        user_dict = user.model_dump(exclude={"id"})

        # Insert and get the _id
        result = await self.user_repository.insert_new_user(user_dict)
        user.id = result.inserted_id

        return user

    async def authenticate_user(self,email:str,password:str)->Optional[UserModel]:
        user_dict = await self.user_repository.find_user_by_username(email)
        if not user_dict :
            return None

        if "status" in user_dict:
            if user_dict["status"] == "UserStatus.ACTIVE":
                user_dict["status"] = "active"
            elif user_dict["status"] == "UserStatus.INACTIVE":
                user_dict["status"] = "inactive"
            elif user_dict["status"] == "UserStatus.SUSPENDED":
                user_dict["status"] = "suspended"

        user = UserModel(**user_dict)
        if not verify_password(password, user.password):
            return None
        return user
