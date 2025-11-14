import re
from datetime import datetime
from app.models.user_model import User

class UserValidator:
    @staticmethod
    def validate_registration(data):
        """
        Valida los datos de registro del usuario.
        Retorna una lista de errores (vacía si todo es válido).
        """
        errores = []

        # Campos obligatorios
        obligatorios = ["nombre", "paterno", "email", "celular", "password"]
        for campo in obligatorios:
            if not data.get(campo):
                errores.append(f"El campo '{campo}' es obligatorio.")

        # Validar nombre y apellidos
        patron_texto = r"^[A-Za-zÁÉÍÓÚáéíóúñÑ\s]+$"
        for campo in ["nombre", "paterno", "materno"]:
            if data.get(campo) and not re.match(patron_texto, data[campo]):
                errores.append(f"El campo '{campo}' solo puede contener letras.")

        # Validar email
        email = data.get("email", "")
        patron_email = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if email and not re.match(patron_email, email):
            errores.append("El correo electrónico no es válido.")

        # Validar celular
        celular = data.get("celular", "")
        if celular and (not re.match(r'^[0-9]{10}$', celular)):
            errores.append("El número celular debe tener 10 dígitos.")

        # Validar contraseña
        password = data.get("password", "")
        if password and (len(password) < 8 or len(password) > 20):
            errores.append("La contraseña debe tener entre 8 y 20 caracteres.")

        # Validar fecha de nacimiento (si se envía)
        fecha_nacimiento = data.get("fecha_nacimiento")
        if fecha_nacimiento:
            try:
                datetime.strptime(fecha_nacimiento, "%Y-%m-%d")
            except ValueError:
                errores.append("La fecha de nacimiento no tiene un formato válido (YYYY-MM-DD).")

        return errores

    @staticmethod
    def check_duplicates(data):
        """
        Valida que email y celular no existan en la base de datos.
        Retorna lista de errores.
        """
        errores = []
        if "email" in data and User.query.filter_by(email=data["email"]).first():
            errores.append("El correo ya está registrado.")

        if "celular" in data and data["celular"] and User.query.filter_by(celular=data["celular"]).first():
            errores.append("El número celular ya está registrado.")

        return errores
