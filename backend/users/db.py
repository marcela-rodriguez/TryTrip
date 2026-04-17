from database import conection
from typing import Dict, Any
from users.models import User,CreateRequest
from bson import ObjectId


def insert_user(user: Dict) -> User:
    result = conection.collection.insert_one(user)
    return User(
        id=str(result.inserted_id),
        names=user.get("names"),
        surnames=user.get("surnames"),
        email=user.get("email"),
        phone_country_code=user.get("phone_country_code"),
        phone_number= user.get("phone_number"),
        pin=user.get("pin")
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
        pin= result.get("pin")
    )
    else:
        return None

def get_user_by_id(id: str) -> User | None:
    result = conection.collection.find_one({"_id": ObjectId(id)})
    print(result)
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
        # Retorna True si encontró al usuario y lo actualizó
        return result.modified_count > 0
    except:
        return False
