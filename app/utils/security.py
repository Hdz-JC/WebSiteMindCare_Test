<<<<<<< HEAD
from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(password: str) -> str:
    return generate_password_hash(password)

def verify_password(hash_pw: str, password: str) -> bool:
    return check_password_hash(hash_pw, password)
from werkzeug.security import generate_password_hash
=======
# app/utils/security.py
from werkzeug.security import generate_password_hash, check_password_hash
>>>>>>> 822eb597927abbb439d3d04c62fe62c222b2787b

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