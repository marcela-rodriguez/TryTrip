import traceback
from os.path import exists
from users.models import CreateRequest, LoginRequest
from users import db
from typing import Dict
from regular_expression import regex
from users import exceptions
import re
import logging
from utils.codes_errors import ErrorCodes
from utils import constants
from jose import JWTError, jwt
from datetime import datetime, timedelta,timezone


def validate_user(user: CreateRequest):
    if re.fullmatch(pattern=regex.EMAIL_REGEX, string=user.email) is None:
        raise exceptions.EmailNotMatch()
    if re.fullmatch(pattern=regex.CODE_COUNTRY_REGEX, string=user.phone_country_code) is None:
        raise exceptions.InvalidCountryFormat()
    if re.fullmatch(pattern=regex.PHONE_NUMBER_REGEX, string=user.phone_number) is None:
        raise exceptions.InvalidPhoneFormat()
    if re.fullmatch(pattern=regex.PIN, string=str(user.pin)) is None:
        raise exceptions.InvalidPinFormat()


def create_user(user: CreateRequest) -> Dict:
    try:
        validate_user(user=user)
        exists_user = db.get_user_by_email(email=user.email)
        if exists_user:
            return {
                "success": False,
                "payload": {},
                "error": [{
                    "code": ErrorCodes.USER_ALREADY_REGISTERED,
                    "title": "User already registered",
                    "message": f"User with email {user.email} is already registered."
                }
                ]
            }
        else:
            user = db.insert_user(user=user.model_dump())
            del user['pin']
            return {
                "success": True,
                "payload": user,
                "error": []
            }
    except exceptions.EmailNotMatch as e:
        return {
            "success": False,
            "payload": {},
            "error": [
                {
                    "code": ErrorCodes.EMAIL_DOES_NOT_COMPLY_WITH_FORMAT,
                    "title": "Email does not comply with format",
                    "message": f"Email {user.email} does not meet the email parameters"
                }
            ]
        }
    except exceptions.InvalidCountryFormat as e:
        return {
            "success": False,
            "payload": {},
            "error": [
                {
                    "code": ErrorCodes.WRONG_COUNTRY_CODE,
                    "title": "Wrong country code",
                    "message": f"Country code {user.phone_country_code} does not meet the required format"
                }
            ]
        }
    except exceptions.InvalidPhoneFormat as e:
        return {
            "success": False,
            "payload": {},
            "error": [
                {
                    "code": ErrorCodes.WRONG_PHONE_FORMAT,
                    "title": "Wrong phone format",
                    "message": f" Phone {user.phone_number} does not meet the required format"
                }
            ]
        }
    except exceptions.InvalidPinFormat as e:
        return {
            "success": False,
            "payload": {},
            "error": [
                {
                    "code": ErrorCodes.WRONG_PIN_FORMAT,
                    "title": "Wrong pin format",
                    "message": f"Pin {user.pin} does not meet the required format"
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
                    "code": ErrorCodes.INTERNAL_SERVER_ERROR,
                    "title": "Internal Server Error.",
                    "message": f"Internal Server Error."
                }
            ]
        }


def validate_login_request(login: LoginRequest):
    if re.fullmatch(pattern=regex.EMAIL_REGEX, string=login.email) is None:
        raise exceptions.EmailNotMatch()
    if re.fullmatch(pattern=regex.PIN, string=str(login.pin)) is None:
        raise exceptions.InvalidPinFormat()

def create_token(data: dict, expires_delta: timedelta, secret_key: str):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc)+ expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret_key, algorithm=constants.ALGORITHM)

def create_tokens(user_id: str):
    access_token = create_token(
        {"user_id": user_id},
        timedelta(minutes=constants.ACCESS_TOKEN_EXPIRE_MINUTES),
        constants.ACCESS_SECRET_KEY
    )
    refresh_token = create_token(
        {"user_id": user_id},
        timedelta(days=constants.REFRESH_TOKEN_EXPIRE_DAYS),
        constants.REFRESH_SECRET_KEY
    )
    return access_token, refresh_token


def authenticate_user(login: LoginRequest) -> Dict:
    try:
        validate_login_request(login=login)
        user= db.get_user_by_email(email=login.email)
        if user.get("email")== login.email and user.get("pin")== login.pin :
            id = str(user.get("_id"))
            access_token, refresh_token = create_tokens(user_id=id)
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

        if user.get("pin") != login.pin:
            print("pint invalid")
            return {
                "success": False,
                "payload": {},
                "error": [{
                    "code": ErrorCodes.INVALID_CREDENTIALS,
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
                    "code": ErrorCodes.USER_NOT_FOUND,
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
                    "code": ErrorCodes.EMAIL_DOES_NOT_COMPLY_WITH_FORMAT,
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
                    "code": ErrorCodes.WRONG_PIN_FORMAT,
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
                    "code": ErrorCodes.INTERNAL_SERVER_ERROR,
                    "title": "Internal Server Error.",
                    "message": f"Internal Server Error."
                }
            ]
        }