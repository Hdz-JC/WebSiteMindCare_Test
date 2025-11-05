# app/services/auth_service.py
from app.services.user_service_interface import UserService
from app.utils.security import hash_password, check_password # Necesitarás crear estas funciones en security.py

class AuthService:
    """
    Servicio de autenticación que gestiona la lógica de login y registro.
    Debe interactuar con un UserService para las operaciones CRUD básicas de usuarios,
    y con funciones de seguridad para el manejo de contraseñas.
    """
    def __init__(self, user_service: UserService):
        """
        Constructor del AuthService.
        Recibe una instancia de UserService para interactuar con los datos de usuario.
        """
        self.user_service = user_service

    def login(self, email: str, raw_password: str):
        """
        Intenta autenticar un usuario con el email y la contraseña proporcionados.
        
        Args:
            email (str): El email del usuario.
            raw_password (str): La contraseña en texto plano (sin hashear).
        
        Returns:
            User: El objeto User si la autenticación es exitosa, None en caso contrario.
        """
        # Primero, busca el usuario por email
        user = self.user_service.authenticate_user(email, password=None) # No pases la password directamente aquí

        if user and check_password(raw_password, user.password):
            # Si el usuario existe y la contraseña hasheada coincide con la guardada
            return user
        return None

    def register(self, paterno: str, materno: str, nombre: str,edad:int, 
                      fecha_nacimiento: str, sexo: str, direccion: str, 
                      celular: str, email: str, raw_password: str):
        """
        Registra un nuevo usuario sin autenticarlo automáticamente.
        Hashea la contraseña antes de pasarla al UserService.
        
        Args:
            (todos los campos del usuario)
            raw_password (str): La contraseña en texto plano.
            
        Returns:
            tuple: (User, list_of_errors)
                   - User: El objeto User si el registro fue exitoso.
                   - list_of_errors: Una lista de errores de registro.
        """
        hashed_password = hash_password(raw_password)

        user, errors = self.user_service.register_user(
            paterno=paterno,
            materno=materno,
            nombre=nombre,
            edad=edad,
            fecha_nacimiento=fecha_nacimiento,
            sexo=sexo,
            direccion=direccion,
            celular=celular,
            email=email,
            password=hashed_password # Pasa la contraseña HASHEADA
        )
        
        return user, errors # Devuelve el usuario registrado o los errores