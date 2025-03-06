from pydantic import BaseModel, constr, EmailStr



class UserRegistrationDto(BaseModel):
    email : EmailStr
    password : constr(min_length=8)
    full_name : constr(min_length=2)

class UserLoginDto(BaseModel):
    email : EmailStr
    password : str

class UserResponseDto(BaseModel):
    id: str
    email: EmailStr
    full_name: str
    status: str

