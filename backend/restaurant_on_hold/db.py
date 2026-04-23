from database.conection import restaurantes_collection
from typing import Dict, Any, List
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
def get_all_restaurant_on_hold() -> List[RestaurantOnHold] | None:
    restaurants = restaurantes_collection.find({})
    restaurants_list = []
    if restaurants is not None:
        for restaurant in restaurants:
            restaurant_obj=RestaurantOnHold(
                id=str(restaurant["_id"]),
                restaurant_name=str(restaurant.get("restaurant_name")),
                link=str(restaurant.get("link")),
                description=str(restaurant.get("description")),
                longitude=float(restaurant.get("longitude")),
                latitude=float(restaurant.get("latitude"))
            )
            restaurants_list.append(restaurant_obj)
        return restaurants_list
    else:
        return None
