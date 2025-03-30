import traceback
from register.models import Register
from register.db import insert_user, get_user_by_email
from register.exceptions import (validate_data, EmailNotMatch, InvalidCountryFormat,
                                 InvalidPhoneFormat, InvalidPinFormat)


def register_user(info: Register) -> dict:
    try:
        user = info.model_dump()
        validate_data(data_user=user)
        response_email = get_user_by_email(email=user.get("email"))
        if response_email:
            return {
                "success": False,
                "payload": {},
                "error": [{
                    "code": 4001,
                    "title": "Usuario ya regitrado",
                    "message": f"usuario con correo {info.email} ya esta registrado "
                }
                ]
            }
        else:
            result = insert_user(user=user)
            return {
                "success": True,
                "payload": result,
                "error": []
            }
    except EmailNotMatch as e:
        return {
            "success": False,
            "payload": {},
            "error": [
                {
                    "code": 4002,
                    "title": "correo no cumple formato",
                    "message": f"correo {info.email} no cumple los parametros de correo"
                }
            ]
        }
    except InvalidCountryFormat as e:
        return {
            "success": False,
            "payload": {},
            "error": [
                {
                    "code": 4003,
                    "title": "codigo de pais incorrecto",
                    "message": f"codigo de pais {info.phone_country_code} no cumple el formato requerido"
                }
            ]
        }
    except InvalidPhoneFormat as e:
        return {
            "success": False,
            "payload": {},
            "error": [
                {
                    "code": 4004,
                    "title": "formato de telefono incorrecto",
                    "message": f" celular {info.phone_number} no cumple el formato requerido"
                }
            ]
        }
    except InvalidPinFormat as e:
        return {
            "success": False,
            "payload": {},
            "error": [
                {
                    "code": 4005,
                    "title": "formato de pin incorrecto",
                    "message": f"pin {info.pin} no cumple el formato requerido"
                }
            ]
        }
    except Exception as e:
        traceback.print_exc()
