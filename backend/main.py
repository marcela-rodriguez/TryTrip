from fastapi import FastAPI
from users.models import CreateRequest, LoginRequest
from users import services
from typing import Dict


app = FastAPI()

@app.post("/users")
def create_user(user:CreateRequest)-> Dict:
    result = services.create_user(user=user)
    return result

@app.get("/login")
def login_user(login:LoginRequest)-> Dict:
    result_login = services.authenticate_user(login=login)
    return result_login