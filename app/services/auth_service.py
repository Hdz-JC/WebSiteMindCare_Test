# services/auth_service.py
from app.models.user_model import User
from app.models import db

def authenticate_user(email, password):
    """
    Busca un usuario que coincida con el email y password.
    Retorna el objeto User si existe, o None si no.
    """
    user = User.query.filter_by(email=email, password=password).first()
    return user

def register_user(paterno, materno, nombre, fecha_nacimiento, sexo,
                  direccion, celular, email, password):
    """
    Registra un usuario nuevo.
    Retorna:
        - User: si se creó correctamente
        - None: si el email ya estaba registrado
    """
    # Verificar si el correo ya existe
    if User.query.filter_by(email=email).first():
        return None

    # Crear el usuario
    user = User(
        paterno=paterno,
        materno=materno,
        nombre=nombre,
        fecha_nacimiento=fecha_nacimiento,
        sexo=sexo,
        direccion=direccion,
        celular=celular,
        email=email,
        password=password
    )

    # Guardar en la base de datos
    db.session.add(user)
    db.session.commit()
    return user