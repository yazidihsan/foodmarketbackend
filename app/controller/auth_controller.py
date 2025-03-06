from venv import create

from fastapi import APIRouter,HTTPException,Depends
from starlette import status

from app.constant.messages import SuccessMessages,ErrorMessages
from app.dto.user_dto import UserRegistrationDto, UserLoginDto
from app.enums.user_status import UserStatus
from app.security.auth import create_access_token
from app.service.auth_service import AuthService
from app.validation.user_validation import validate_registration_data, validate_login_data

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register")
async def register_user(user_data:UserRegistrationDto):
    try:
        validate_data = validate_registration_data(user_data)
        auth_service = AuthService()
        user = await auth_service.create_user(validate_data.model_dump())
        return {"message": SuccessMessages.USER_CREATED,"user":user}

    except ValueError as e:
        raise HTTPException(status_code=401,detail=str(e))

@router.post("/login")
async def login_user(login_data:UserLoginDto):
    try:
        validate_data = validate_login_data(login_data)
        auth_service = AuthService()
        user = await auth_service.authenticate_user(
            validate_data.email,
            validate_data.password
        )
        if not user:
            raise HTTPException(
                status_code=401,
                detail=ErrorMessages.INVALID_CREDENTIALS
            )

        access_token = create_access_token(data={"sub":user.email})
        return {
            "message":SuccessMessages.LOGIN_SUCCESS,
            "access_token":access_token,
            "token_type":"bearer"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


def convert_string_to_enum(status_string: str) -> UserStatus:
    for status_member in UserStatus:
        if status_member.value == status_string:
            return status_member
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid User Status")


