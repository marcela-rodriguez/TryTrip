# Expresión regular para validar correos electrónicos
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
# Regex para código de país (ej: +57, +1, +34)
CODE_COUNTRY_REGEX = r'^\+\d{1,3}$'
# Regex para número de celular (10 dígitos)
PHONE_NUMBER_REGEX = r'^\d{10}$'
PIN = r'^\d{4}$'
