from pydantic import BaseModel

class CreateRestaurantOnHold(BaseModel):
    restaurant_name: str
    link:str
    description: str
    longitude: float
    latitude: float

class RestaurantOnHold(BaseModel):
    id:str
    restaurant_name: str
    link:str
    description: str
    longitude: float
    latitude: float