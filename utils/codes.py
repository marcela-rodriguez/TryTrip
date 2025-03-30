from pydantic import BaseModel


class ErrorRequest(BaseModel):
    errors_codes: int


errors_codes = {
    4001: "El usuario ya registrado",
    4002: "correo no cumple formato",
    4003: "codigo de pais incorrecto",
    4004: "formato de telefono incorrecto",
    4005: "formato de pin incorrecto",

}
