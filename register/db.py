from database import conection
from typing import Dict, Any


def insert_user(user: Dict[str, Any]):
    result = conection.collection.insert_one(user)
    user["_id"] = str(result.inserted_id)
    return user


def get_user_by_email(email: str) -> Dict:
    result = conection.collection.find_one({"email": email})
    if result:
        return result
    else:
        return {}
