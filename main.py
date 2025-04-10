from fastapi import FastAPI
from users.models import User
from users import services
from typing import Dict


app = FastAPI()

@app.post("/users")
def create_user(creare_date:User)-> Dict:
    result = services.create_user(info=creare_date)
    return result


