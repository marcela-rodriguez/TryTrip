from database import conection
from typing import Dict, Any

def get_user_by_email(email: str) -> Dict:
    user = conection.collection.find_one({"email": email})
    if user:
        return user
    else:
        return {}