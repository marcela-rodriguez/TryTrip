import traceback
from users.models import User
from users import db
from users import exceptions
from utils.codes import ErrorRequest
from typing import Dict


def create_user(info: User) -> Dict:
    try:
        user = info.model_dump()
        exceptions.validate_data(data_user=info)
        response_email = db.get_user_by_email(email=user.get("email"))
        if response_email:
            return {
                "success": False,
                "payload": {},
                "error": [{
                    "code": ErrorRequest.USER_ALREADY_REGISTERED,
                    "title": "User already registered",
                    "message": f"User with email {info.email} is already registered."
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
                    "message": f"Email {info.email} does not meet the email parameters"
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
                    "message": f"Country code {info.phone_country_code} does not meet the required format"
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
                    "message": f" Phone {info.phone_number} does not meet the required format"
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
                    "message": f"Pin {info.pin} does not meet the required format"
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
