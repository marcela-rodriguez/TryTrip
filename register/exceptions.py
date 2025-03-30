from typing import Dict, List
from expresion_regular import reges_email, reges_pin, reges_phone_number, reges_phone_country_code
import re


class EmailNotMatch(Exception): ...


class InvalidCountryFormat(Exception): ...


class InvalidPhoneFormat(Exception): ...


class InvalidPinFormat(Exception): ...


def validate_data(data_user: Dict):
    if re.fullmatch(pattern=reges_email.EMAIL_REGEX, string=data_user.get("email")) is None:
        raise EmailNotMatch()
    if re.fullmatch(pattern=reges_phone_country_code.CODIGO_PAIS_REGEX, string=data_user.get("phone_country_code")) is None:
        raise InvalidCountryFormat()
    if re.fullmatch(pattern=reges_phone_number.NUMERO_CELULAR_REGEX, string=data_user.get("phone_number")) is None:
        raise InvalidPhoneFormat()
    if re.fullmatch(pattern=reges_pin.PIN, string=str(data_user.get("pin"))) is None:
        raise InvalidPinFormat()
