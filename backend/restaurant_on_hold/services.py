from restaurant_on_hold.models import RestaurantOnHold,CreateRestaurantOnHold
from restaurant_on_hold import db

def create_restaurant_on_hold(restaurant:CreateRestaurantOnHold)->RestaurantOnHold:
    restaurant_result=db.insert_restaurant_on_hold(restaurant=restaurant)
    return restaurant_result


