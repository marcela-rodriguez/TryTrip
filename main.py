from fastapi import FastAPI
from register.models import Register
from register.register import register_user


app = FastAPI()

@app.post("/register")
def register(register_date: Register)-> dict:
    result = register_user(info=register_date)
    return result


