from restaurant_on_hold.models import RestaurantOnHold,CreateRestaurantOnHold
from restaurant_on_hold import db
from typing import Dict, Any, List
from restaurant_on_hold import exceptions


def create_restaurant_on_hold(restaurant:CreateRestaurantOnHold)->RestaurantOnHold:
    restaurant_result=db.insert_restaurant_on_hold(restaurant=restaurant)
    return restaurant_result


def get_restaurants_on_hold() -> List[RestaurantOnHold] | None:
    restaurants=db.get_all_restaurant_on_hold()
    if restaurants:
        return restaurants
    else:
        raise exceptions.RestaurantsOnHoldNotFounds()