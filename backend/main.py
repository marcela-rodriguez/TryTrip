from fastapi import FastAPI
from login.models import LoginRequest
from login.services import authenticate_user
from users.models import User
from users import services
from typing import Dict


app = FastAPI()

@app.post("/users")
def create_user(user:User)-> Dict:
    result = services.create_user(user=user)
    return result

@app.get("/login")
def login_user(login:LoginRequest)-> Dict:
    result_login = authenticate_user(login)
    return result_login