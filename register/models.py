from pydantic import BaseModel


class Register(BaseModel):
    names: str
    surnames: str
    email: str
    phone_country_code: str
    phone_number: str
    pin: int
