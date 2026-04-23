from database.conection import restaurantes_collection
from typing import Dict, Any
from restaurant_on_hold.models import RestaurantOnHold,CreateRestaurantOnHold

def insert_restaurant_on_hold(restaurant: CreateRestaurantOnHold) -> RestaurantOnHold:
    restaurant_db=restaurant.model_dump()
    result = restaurantes_collection.insert_one(restaurant_db)
    return RestaurantOnHold(
        id=str(result.inserted_id),
        restaurant_name=str(restaurant.restaurant_name),
        link=str(restaurant.link),
        description=str(restaurant.description),
        longitude=float(restaurant.longitude),
        latitude=float(restaurant.latitude)
    )
