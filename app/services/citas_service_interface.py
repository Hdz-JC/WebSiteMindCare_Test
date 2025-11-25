from abc import ABC, abstractmethod

class CitaService(ABC):
    
    @abstractmethod
    def agendar_cita(self,data):
        pass

    @abstractmethod
    def obtener_citas(self):
        pass
    
    