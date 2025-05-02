import logging
import traceback
from login.models import LoginRequest
from login import db
from utils.codes import ErrorRequest
from typing import Dict
from regular_expression import regex
from utils import constants
from login import exceptions
import re
from jose import JWTError, jwt
from datetime import datetime, timedelta,timezone

def validate_login(login: LoginRequest):
    if re.fullmatch(pattern=regex.EMAIL_REGEX, string=login.email) is None:
        raise exceptions.EmailNotMatch()
    if re.fullmatch(pattern=regex.PIN, string=str(login.pin)) is None:
        raise exceptions.InvalidPinFormat()

def post_token(data: dict, expires_delta: timedelta, secret_key: str):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc)+ expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret_key, algorithm=constants.ALGORITHM)

def post_tokens(user_id: str):
    access_token = post_token(
        {"user_id": user_id},
        timedelta(minutes=constants.ACCESS_TOKEN_EXPIRE_MINUTES),
        constants.ACCESS_SECRET_KEY
    )
    refresh_token = post_token(
        {"user_id": user_id},
        timedelta(days=constants.REFRESH_TOKEN_EXPIRE_DAYS),
        constants.REFRESH_SECRET_KEY
    )
    return access_token, refresh_token


def authenticate_user(login: LoginRequest) -> Dict:
    try:
        validate_login(login=login)
        user= db.get_user_by_email(email=login.email)
        if user.get("email")== login.email and user.get("pin")== login.pin :
            id = str(user.get("_id"))
            access_token, refresh_token = post_tokens(user_id=id)
            return_tokens = {
                "token_type": "bearer",
                "access_token": access_token,
                "refresh_token": refresh_token

            }
            return {
                "success": True,
                "payload":return_tokens ,
                "error": []
            }
        if user.get("email") != login.email:
            print("email invalid")
            return {
                "success": False,
                "payload": {},
                "error": [{
                    "code": ErrorRequest.INVALID_CREDENTIALS,
                    "title": "Invalid credentials",
                    "message": f"Invalid credentials"
                }
                ]
            }
        if user.get("pin") != login.pin:
            print("pint invalid")
            return {
                "success": False,
                "payload": {},
                "error": [{
                    "code": ErrorRequest.INVALID_CREDENTIALS,
                    "title": "Invalid credentials",
                    "message": f"Invalid credentials"
                }
                ]
            }


        else:
            return {
                "success": False,
                "payload": {},
                "error": [{
                    "code": ErrorRequest.USER_NOT_FOUND,
                    "title": "User not found",
                    "message": f"User not found."
                }
                ]
            }

    except exceptions.EmailNotMatch as e:
        return {
            "success": False,
            "payload": {},
            "error": [
                {
                    "code": ErrorRequest.EMAIL_DOES_NOT_COMPLY_WITH_FORMAT,
                    "title": "Email does not comply with format",
                    "message": f"Email {login.email} does not meet the email parameters"
                }
            ]
        }
    except exceptions.InvalidPinFormat as e:
        return {
            "success": False,
            "payload": {},
            "error": [
                {
                    "code": ErrorRequest.WRONG_PIN_FORMAT,
                    "title": "Wrong pin format",
                    "message": f"Pin {login.pin} does not meet the required format"
                }
            ]
        }
    except Exception as e:
        traceback.print_exc()
        print(e)
        return {
            "success": False,
            "payload": {},
            "error": [
                {
                    "code": ErrorRequest.INTERNAL_SERVER_ERROR,
                    "title": "Internal Server Error.",
                    "message": f"Internal Server Error."
                }
            ]
        }
