from database import conection
from typing import Dict, Any
from users.models import User,CreateRequest
from bson import ObjectId


def insert_user(user: CreateRequest) -> User:
    user_dict=user.model_dump()
    result = conection.collection.insert_one(user_dict)
    return User(
        id=str(result.inserted_id),
        names=user_dict.get("names"),
        surnames=user_dict.get("surnames"),
        email=user_dict.get("email"),
        phone_country_code=user_dict.get("phone_country_code"),
        phone_number= user_dict.get("phone_number"),
        pin=user_dict.get("pin")
    )


def get_user_by_email(email: str) -> User | None:
    result = conection.collection.find_one({"email": email})
    if result:
        return  User(
        id=str(result.get("_id")),
        names=result.get("names"),
        surnames=result.get("surnames"),
        email=result.get("email"),
        phone_country_code=result.get("phone_country_code"),
        phone_number= result.get("phone_number"),
        pin=result.get("pin")
    )
    else:
        return None

def get_user_by_id(id: str) -> User | None:
    result = conection.collection.find_one({"_id": ObjectId(id)})
    if result:
        return  User(
        id=str(result.get("_id")),
        names=result.get("names"),
        surnames=result.get("surnames"),
        email=result.get("email"),
        phone_country_code=result.get("phone_country_code"),
        phone_number= result.get("phone_number"),
        pin= result.get("pin")
    )
    else:
        return None

def update_user_pin(user_id: str, new_pin: str) -> bool:
    try:
        result = conection.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"pin": new_pin}}
        )
        return result.modified_count > 0
    except:
        return False
