from pydantic import ValidationError

from app.dto.user_dto import UserRegistrationDto, UserLoginDto


def validate_registration_data(data: dict | UserRegistrationDto) -> UserRegistrationDto:
    try:
        if isinstance(data,UserRegistrationDto):
            return data

        return UserRegistrationDto(**data)
    except ValidationError as e :
        raise ValueError(str(e))

def validate_login_data(data:dict | UserLoginDto)-> UserLoginDto :
    try:
        if isinstance(data,UserLoginDto):
            return data
        return UserLoginDto(**data)
    except ValidationError as e:
        raise ValueError(str(e))



