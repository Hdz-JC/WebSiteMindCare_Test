from abc import ABC, abstractmethod

class NotasService(ABC):
    
    @abstractmethod
    def agregar_nota(self, idcita, contenido, user, titulo):
        pass

    @abstractmethod
    def obtener_notas_por_usuario(self, user):
        pass
