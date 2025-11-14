from abc import ABC, abstractmethod

class PsicologoService(ABC):
    
    @abstractmethod
    def obtener_psicologo(self):
        """Devuelve el psicólogo único registrado en el sistema"""
        pass
