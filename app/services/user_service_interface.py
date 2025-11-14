# app/services/user_service_interface.py
from abc import ABC, abstractmethod

class UserService(ABC):
    @abstractmethod
    def authenticate_user(self, email, password):
        pass

    @abstractmethod
    def register_user(self, paterno, materno, nombre, edad, fecha_nacimiento, sexo,
                      direccion, celular, email, password):
        pass