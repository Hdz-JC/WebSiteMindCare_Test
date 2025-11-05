# app/utils/security.py
from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(password: str) -> str:
    """
    Hashea una contraseña usando un algoritmo seguro.
    """
    return generate_password_hash(password)

def check_password(raw_password: str, hashed_password: str) -> bool:
    """
    Verifica si una contraseña en texto plano coincide con una contraseña hasheada.
    """
    return check_password_hash(hashed_password, raw_password)