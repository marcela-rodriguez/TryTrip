from fastapi import FastAPI
from users.models import User
from users import services
from typing import Dict


app = FastAPI()

@app.post("/users")
def create_user(user:User)-> Dict:
    result = services.create_user(user=user)
    return result
