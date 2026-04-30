from fastapi import FastAPI,Depends
from users.models import CreateRequest, LoginRequest,ChangePasswordRequest
from users import services
from typing import Dict
from utils.codes_errors import ErrorCodes
import traceback
from users import exceptions
from fastapi.security import HTTPBearer
from restaurant_on_hold import exceptions as restaurant_exception, models, services as restaurant_services
from pymongo.errors import OperationFailure


app = FastAPI()

@app.post("/users")
def create_user(user:CreateRequest)-> Dict:
    try:
        result = services.create_user(user=user)
        print(result)
        if result:
            user = result.model_dump(exclude={"pin"})
            return {
                "success": True,
                "payload": user,
                "error": []
            }
    except exceptions.UserAlreadyRegistered as e:
            return {
                "success": False,
                "payload": {},
                "error": [{
                    "code": ErrorCodes.USER_ALREADY_REGISTERED,
                    "title": "User already registered",
                    "message": f"User with email {user.email} is already registered."
                }
                ]
            }
    except exceptions.EmailNotMatch as e:
        return {
            "success": False,
            "payload": {},
            "error": [
                {
                    "code": ErrorCodes.EMAIL_DOES_NOT_COMPLY_WITH_FORMAT,
                    "title": "Email does not comply with format",
                    "message": f"Email {user.email} does not meet the email parameters"
                }
            ]
        }
    except exceptions.InvalidCountryFormat as e:
        return {
            "success": False,
            "payload": {},
            "error": [
                {
                    "code": ErrorCodes.WRONG_COUNTRY_CODE,
                    "title": "Wrong country code",
                    "message": f"Country code {user.phone_country_code} does not meet the required format"
                }
            ]
        }
    except exceptions.InvalidPhoneFormat as e:
        return {
            "success": False,
            "payload": {},
            "error": [
                {
                    "code": ErrorCodes.WRONG_PHONE_FORMAT,
                    "title": "Wrong phone format",
                    "message": f" Phone {user.phone_number} does not meet the required format"
                }
            ]
        }
    except exceptions.InvalidPinFormat as e:
        return {
            "success": False,
            "payload": {},
            "error": [
                {
                    "code": ErrorCodes.WRONG_PIN_FORMAT,
                    "title": "Wrong pin format",
                    "message": f"Pin {user.pin} does not meet the required format"
                }
            ]
        }
    except Exception as e:
        traceback.print_exc()
        return {
            "success": False,
            "payload": {},
            "error": [
                {
                    "code": ErrorCodes.INTERNAL_SERVER_ERROR,
                    "title": "Internal Server Error.",
                    "message": f"Internal Server Error."
                }
            ]
        }

security = HTTPBearer()
@app.patch("/change_password")
def change_password(request: ChangePasswordRequest, auth=Depends(security)) -> Dict:
    try:
        token: str = auth.credentials
        services.change_password(token=token, new_password=request)
        return {
            "success": True,
            "payload": {"message": "Password updated successfully"},
            "error": []
        }

    except exceptions.TokenExpired as e:
        return {
            "success": False,
            "payload": {},
            "error": [{
                "code": ErrorCodes.TOKEN_EXPIRED,
                "title": "Token Expired",
                "message": "Your session has expired. Please login again."
            }]
        }
    except exceptions.InvalidToken as e:
        return {
            "success": False,
            "payload": {},
            "error": [{
                "code": ErrorCodes.INVALID_TOKEN,
                "title": "Invalid Token",
                "message": "The provided token is invalid or malformed."
            }]
        }
    except exceptions.InvalidCredentialsToken as e:
        return {
            "success": False,
            "payload": {},
            "error": [{
                "code": ErrorCodes.INVALID_CREDENTIALS,
                "title": "Invalid Credentials",
                "message": "Token does not contain valid user information."
            }]
        }
    except exceptions.InvalidPinFormat as e:
        return {
            "success": False,
            "payload": {},
            "error": [{
                "code": ErrorCodes.WRONG_PIN_FORMAT,
                "title": "Wrong pin format",
                "message": "The new pin does not meet the required 4-digit format."
            }]
        }
    except exceptions.UserNotFound as e:
        return {
            "success": False,
            "payload": {},
            "error": [{
                "code": ErrorCodes.USER_NOT_FOUND,
                "title": "User not found",
                "message": "The user associated with this token no longer exists."
            }]
        }
    except exceptions.CurrentlyUsedPassword as e:
        return {
            "success": False,
            "payload": {},
            "error": [{
                "code": ErrorCodes.CURRENTLY_USED_PASSWORD,
                "title": "Password already in use",
                "message": "The new PIN cannot be the same as the current one."
            }]
        }
    except exceptions.UserUpdateFailed as e:
        return {
            "success": False,
            "payload": {},
            "error": [{
                "code": ErrorCodes.UPDATE_FAILED,
                "title": "Update Failed",
                "message": "Could not update the PIN in the database."
            }]
        }
    except Exception as e:
        traceback.print_exc()
        return {
            "success": False,
            "payload": {},
            "error": [{
                "code": ErrorCodes.INTERNAL_SERVER_ERROR,
                "title": "Internal Server Error",
                "message": "An unexpected error occurred."
            }]
        }

@app.post("/login")
def login_user(login:LoginRequest)-> Dict:
    try:
        result_login = services.authenticate_user(login=login)
        if result_login:
            id = str(result_login.id)
            access_token, refresh_token = services.create_tokens(user_id=id)
            return_tokens = {
                "token_type": "bearer",
                "access_token": access_token,
                "refresh_token": refresh_token

            }
            return {
                "success": True,
                "payload": return_tokens,
                "error": []
            }

    except exceptions.InvalidCredentials as e:
        return {
            "success": False,
            "payload": {},
            "error": [{
                "code": ErrorCodes.INVALID_CREDENTIALS,
                "title": "Invalid credentials",
                "message": f"Invalid credentials"
            }
            ]
        }
    except exceptions.UserNotFound as e:
        return {
            "success": False,
            "payload": {},
            "error": [{
                "code": ErrorCodes.USER_NOT_FOUND,
                "title": "User not found",
                "message": f"User not found."
            }
            ]
        }
    except exceptions.EmailNotMatch as e:
        return {
            "success": False,
            "payload": {},
            "error": [
                {
                    "code": ErrorCodes.EMAIL_DOES_NOT_COMPLY_WITH_FORMAT,
                    "title": "Email does not comply with format",
                    "message": f"Email {login.email} does not meet the email parameters"
                }
            ]
        }
    except exceptions.InvalidPinFormat as e:
        return {
            "success": False,
            "payload": {},
            "error": [
                {
                    "code": ErrorCodes.WRONG_PIN_FORMAT,
                    "title": "Wrong pin format",
                    "message": f"Pin {login.pin} does not meet the required format"
                }
            ]
        }
    except Exception as e:
        traceback.print_exc()
        return {
            "success": False,
            "payload": {},
            "error": [
                {
                    "code": ErrorCodes.INTERNAL_SERVER_ERROR,
                    "title": "Internal Server Error.",
                    "message": f"Internal Server Error."
                }
            ]
        }

@app.post("/create_restaurant_on_hold")
def create_restaurant_on_hold(restaurant:models.CreateRestaurantOnHold)-> Dict:
    try:
        result_create_restaurant = restaurant_services.create_restaurant_on_hold(restaurant=restaurant)
        if result_create_restaurant:
            restaurant = result_create_restaurant.model_dump()
            return {
                "success": True,
                "payload": restaurant,
                "error": []
            }

    except Exception as e:
        traceback.print_exc()
        print(e)
        return {
            "success": False,
            "payload": {},
            "error": [
                {
                    "code": ErrorCodes.INTERNAL_SERVER_ERROR,
                    "title": "Internal Server Error.",
                    "message": f"Internal Server Error."
                }
            ]
        }
@app.get("/restaurant_on_hold")
def get_restaurant_on_hold()-> Dict:
    try:
        result_get_restaurants = restaurant_services.get_restaurants_on_hold()
        if result_get_restaurants:
            restaurants = result_get_restaurants
            return {
                "success": True,
                "payload": {"restaurants":restaurants},
                "error": []
            }
    except restaurant_exception.RestaurantsOnHoldNotFounds as e:
        return {
            "success": False,
            "payload": {},
            "error": [{
                "code": ErrorCodes.RESTAURANTS_NOT_FOUND,
                "title": "Restaurants not found",
                "message": "There are no restaurants registered in list yet."
            }]
        }

    except Exception as e:
        traceback.print_exc()
        print(e)
        return {
            "success": False,
            "payload": {},
            "error": [
                {
                    "code": ErrorCodes.INTERNAL_SERVER_ERROR,
                    "title": "Internal Server Error.",
                    "message": f"Internal Server Error."
                }
            ]
        }


@app.get("/restaurant_on_hold/nearby")
def get_nearby_restaurants(longitude: float, latitude: float, distance: int = 5000) -> Dict:
    try:
        #radio (por defecto 5km)
        result_restaurants = restaurant_services.get_nearby_restaurants(
            longitude=longitude,
            latitude=latitude,
            radius_meters=distance
        )

        return {
            "success": True,
            "payload": {
                "restaurants": result_restaurants
            },
            "error": []
        }

    except restaurant_exception.RestaurantsOnHoldNotFounds:
        return {
            "success": False,
            "payload": {},
            "error": [{
                "code": ErrorCodes.RESTAURANTS_NOT_FOUND,
                "title": "No restaurants nearby",
                "message": f"We couldn't find any restaurants within {distance} meters of your location."
            }]
        }
    except  OperationFailure as e:
        traceback.print_exc()
        return {
            "success": False,
            "payload": {},
            "error": [{
                "code": ErrorCodes.GEO_ERROR,
                "title": "Invalid Coordinates",
                "message": "The coordinates provided are out of the allowed geographic bounds (Latitude -90 to 90, Longitude -180 to 180)."
            }]
        }

    except Exception as e:
        traceback.print_exc()
        return {
            "success": False,
            "payload": {},
            "error": [{
                "code": ErrorCodes.INTERNAL_SERVER_ERROR,
                "title": "Internal Server Error.",
                "message": "An error occurred while searching for nearby restaurants."
            }]
        }