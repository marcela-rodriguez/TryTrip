from database.conection import usuarios_collection
from typing import Dict, Any
from users.models import User


def insert_user(user: Dict) -> User:
    result = usuarios_collection.insert_one(user)
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
    result = usuarios_collection.find_one({"email": email})
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

