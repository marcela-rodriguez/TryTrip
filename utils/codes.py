from enum import Enum


class ErrorRequest(Enum):
    USER_ALREADY_REGISTERED = 4001,
    EMAIL_DOES_NOT_COMPLY_WITH_FORMAT = 4002,
    WRONG_COUNTRY_CODE = 4003,
    WRONG_PHONE_FORMAT = 4004,
    WRONG_PIN_FORMAT = 4005,
    INTERNAL_SERVER_ERROR = 4006.

