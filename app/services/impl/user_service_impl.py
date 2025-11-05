# app/services/impl/user_service_impl.py
from app.models.user_model import User
from app.models import db
from app.services.user_service_interface import UserService

class UserServiceImpl(UserService):
    
    # MODIFICACIÓN IMPORTANTE AQUÍ
    def authenticate_user(self, email: str, password=None): # El 'password' ya no se usa para filtrar directamente
        """
        Busca un usuario por su email.
        Retorna el objeto User si existe, o None si no.
        La verificación de la contraseña se hace en el AuthService.
        """
        # Solo busca por email. El campo 'password' en la firma es por compatibilidad con la interfaz,
        # pero aquí no se usa para la consulta.
        user = User.query.filter_by(email=email).first() 
        return user

    def register_user(self, paterno, materno, nombre, edad, fecha_nacimiento, sexo,
                      direccion, celular, email, password):
        """
        Registra un usuario nuevo.
        Recibe la 'password' ya hasheada desde el AuthService.
        Retorna:
            - User: si se creó correctamente
            - None: si el email ya estaba registrado
        """
        errors = [] 

        if User.query.filter_by(email=email).first():
            errors.append("email")

        if celular and User.query.filter_by(celular=celular).first():
            errors.append("celular")

        if errors:
            return None, errors

        # Crear el usuario
        user = User(
            paterno=paterno,
            materno=materno,
            nombre=nombre,
            edad=edad,
            fecha_nacimiento=fecha_nacimiento,
            sexo=sexo,
            direccion=direccion,
            celular=celular,
            email=email,
            password=password # ¡Aquí 'password' DEBE ser la contraseña HASHEADA!
        )

        # Guardar en la base de datos
        db.session.add(user)
        db.session.commit()
        return user, None