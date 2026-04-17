import traceback
from os.path import exists
from users.models import CreateRequest, LoginRequest, User, ChangePasswordRequest
from users import db
from typing import Dict
from regular_expression import regex
from users import exceptions
import re
import logging
from utils.codes_errors import ErrorCodes
from utils import constants
from jose import JWTError, jwt,ExpiredSignatureError
from datetime import datetime, timedelta,timezone
from bson import ObjectId


def validate_user(user: CreateRequest):
    if re.fullmatch(pattern=regex.EMAIL_REGEX, string=user.email) is None:
        raise exceptions.EmailNotMatch()
    if re.fullmatch(pattern=regex.CODE_COUNTRY_REGEX, string=user.phone_country_code) is None:
        raise exceptions.InvalidCountryFormat()
    if re.fullmatch(pattern=regex.PHONE_NUMBER_REGEX, string=user.phone_number) is None:
        raise exceptions.InvalidPhoneFormat()
    if re.fullmatch(pattern=regex.PIN, string=str(user.pin)) is None:
        raise exceptions.InvalidPinFormat()


def create_user(user: CreateRequest) -> User:
        validate_user(user=user)
        exists_user = db.get_user_by_email(email=user.email)
        if exists_user is None:
            user = db.insert_user(user=user.model_dump())
            return user
        else:
            raise exceptions.UserAlreadyRegistered()


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


def authenticate_user(login: LoginRequest) -> User:
        validate_login_request(login=login)
        user= db.get_user_by_email(email=login.email)
        print(user)
        if not user:
            raise exceptions.UserNotFound()
        if user.pin != login.pin:
            print("pint invalid")
            raise exceptions.InvalidCredentials()

        return user


def authenticate_token(token: str, secre: str)->str:
    try:
        payload = jwt.decode(token, secre, algorithms=[constants.ALGORITHM])
        user_id = payload.get("user_id")

        if user_id is None:
            raise exceptions.InvalidCredentialsToken()#no ceunta con el algoritmo

        if not ObjectId.is_valid(user_id):
            raise exceptions.InvalidToken()  # O una excepción de "ID malformado"
        return user_id
    except ExpiredSignatureError:
    # Específicamente cuando el tiempo 'exp' ya pasó
        raise exceptions.TokenExpired()

    except JWTError:
        raise exceptions.InvalidToken()

def change_password(token:str,new_password:ChangePasswordRequest)->User:
    user_id=authenticate_token(token=token,secre=constants.ACCESS_SECRET_KEY)
    print(user_id)
    if re.fullmatch(pattern=regex.PIN, string=str(new_password)) is None:
        raise exceptions.InvalidPinFormat()
    user=db.get_user_by_id(id=user_id)
    if not user:
         raise exceptions.UserNotFound()
    print(user.pin)
    print(new_password)
    if user.pin == new_password:
         raise exceptions.CurrentlyUsedPassword()
    user_db=db.update_user_pin(user_id=user_id,new_pin=new_password)
    if not user_db:
        raise exceptions.UserUpdateFailed()

    user.pin = new_password
    return user





