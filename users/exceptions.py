from regular_expression import regex
from users.models import User
import re


class EmailNotMatch(Exception): ...


class InvalidCountryFormat(Exception): ...


class InvalidPhoneFormat(Exception): ...


class InvalidPinFormat(Exception): ...


def validate_data(data_user: User):
    if re.fullmatch(pattern=regex.EMAIL_REGEX, string=data_user.email) is None:
        raise EmailNotMatch()
    if re.fullmatch(pattern=regex.CODE_COUNTRY_REGEX, string=data_user.phone_country_code) is None:
        raise InvalidCountryFormat()
    if re.fullmatch(pattern=regex.PHONE_NUMBER_REGEX, string=data_user.phone_number) is None:
        raise InvalidPhoneFormat()
    if re.fullmatch(pattern=regex.PIN, string=str(data_user.pin)) is None:
        raise InvalidPinFormat()
