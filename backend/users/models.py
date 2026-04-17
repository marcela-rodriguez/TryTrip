from pydantic import BaseModel


class CreateRequest(BaseModel):
    names: str
    surnames: str
    email: str
    phone_country_code: str
    phone_number: str
    pin: int

class LoginRequest(BaseModel):
    email: str
    pin: int

class User(BaseModel):
    id:str
    names: str
    surnames: str
    email: str
    phone_country_code: str
    phone_number: str
    pin: int

class ChangePasswordRequest(BaseModel):
    new_password: int
