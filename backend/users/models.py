from pydantic import BaseModel


class CreateRequest(BaseModel):
    names: str
    surnames: str
    email: str
    phone_country_code: str
    phone_number: str
    pin: str

class LoginRequest(BaseModel):
    email: str
    pin: str

class User(BaseModel):
    id:str
    names: str
    surnames: str
    email: str
    phone_country_code: str
    phone_number: str
    pin: str

class ChangePasswordRequest(BaseModel):
    new_password: str
