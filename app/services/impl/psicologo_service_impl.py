from app.models.user_model import User
from app.models import db
from app.services.psicologo_service_interface import PsicologoService

class PsicologoServiceImpl(PsicologoService):

    def obtener_psicologo(self):
        """Devuelve el primer psicólogo disponible (por simplicidad)"""
        try:
            psicologo = User.query.filter_by(rol='psicologo').first()
            if not psicologo:
                return {"error": "No hay psicólogos registrados"}

            return {
                "idusuario": psicologo.id,
                "nombre": psicologo.nombre,
                "apellidopaterno": psicologo.paterno,
                "apellidomaterno": psicologo.materno,
                "correo": psicologo.email
            }
        except Exception as e:
            return {"error": f"Error al obtener psicólogo: {str(e)}"}

