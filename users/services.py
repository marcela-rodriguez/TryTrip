import traceback
from users.models import User
from users import db
from utils.codes import ErrorRequest
from typing import Dict
from regular_expression import regex
from users import exceptions
import re

def validate_user(data_user: User):
    if re.fullmatch(pattern=regex.EMAIL_REGEX, string=data_user.email) is None:
        raise exceptions.EmailNotMatch()
    if re.fullmatch(pattern=regex.CODE_COUNTRY_REGEX, string=data_user.phone_country_code) is None:
        raise exceptions.InvalidCountryFormat()
    if re.fullmatch(pattern=regex.PHONE_NUMBER_REGEX, string=data_user.phone_number) is None:
        raise exceptions.InvalidPhoneFormat()
    if re.fullmatch(pattern=regex.PIN, string=str(data_user.pin)) is None:
        raise exceptions.InvalidPinFormat()

def create_user(data_user: User) -> Dict:
    try:
        user = data_user.model_dump()
        validate_user(data_user=data_user)
        response_email = db.get_user_by_email(email=user.get("email"))
        if response_email:
            return {
                "success": False,
                "payload": {},
                "error": [{
                    "code": ErrorRequest.USER_ALREADY_REGISTERED,
                    "title": "User already registered",
                    "message": f"User with email {data_user.email} is already registered."
                }
                ]
            }
        else:
            info_user = db.insert_user(user=user)
            del info_user['pin']
            return {
                "success": True,
                "payload": info_user,
                "error": []
            }
    except exceptions.EmailNotMatch as e:
        return {
            "success": False,
            "payload": {},
            "error": [
                {
                    "code": ErrorRequest.EMAIL_DOES_NOT_COMPLY_WITH_FORMAT,
                    "title": "Email does not comply with format",
                    "message": f"Email {data_user.email} does not meet the email parameters"
                }
            ]
        }
    except exceptions.InvalidCountryFormat as e:
        return {
            "success": False,
            "payload": {},
            "error": [
                {
                    "code": ErrorRequest.WRONG_COUNTRY_CODE,
                    "title": "Wrong country code",
                    "message": f"Country code {data_user.phone_country_code} does not meet the required format"
                }
            ]
        }
    except exceptions.InvalidPhoneFormat as e:
        return {
            "success": False,
            "payload": {},
            "error": [
                {
                    "code": ErrorRequest.WRONG_PHONE_FORMAT,
                    "title": "Wrong phone format",
                    "message": f" Phone {data_user.phone_number} does not meet the required format"
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
                    "message": f"Pin {data_user.pin} does not meet the required format"
                }
            ]
        }
    except Exception as e:
        traceback.print_exc()
        return {
            "success": False,
            "payload": {},
            "error": [
                {
                    "code": ErrorRequest.INTERNAL_SERVER_ERROR,
                    "title": "Internal Server Error.",
                    "message": f"Internal Server Error: {e}."
                }
            ]
        }
