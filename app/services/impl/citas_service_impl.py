from app.models.citas_model import Cita
from app.models.user_model import User
from app.models import db
from app.services.citas_service_interface import CitaService
from datetime import date,datetime

class CitaServiceImpl(CitaService):
    
    def agendar_cita(self, data):
        try:
            psicologo = User.query.filter_by(rol='psicologo').first()
            hoy = date.today()
            fecha_cita = datetime.strptime(data["fecha"], "%Y-%m-%d").date()

            # Si la cita es hoy, cambia estado a 'aceptada', si no, 'pendiente'
            estado_cita = "aceptada" if fecha_cita == hoy else "pendiente"

            if not psicologo:
                return {"error": "No hay psicólogo registrado en el sistema"}

            nueva_cita = Cita(
                fkidusuario=data["fkidusuario"],
                fkidpsicologo=psicologo.id,
                fecha=data["fecha"],
                horainicio=data["horainicio"],
                horafin=data["horafin"],
                estado=estado_cita,
                descripcioncancelado=data.get("descripcioncancelado")
            )

            db.session.add(nueva_cita)
            db.session.commit()
            return {"message": "Cita creada correctamente", "idcita": nueva_cita.idcita}
        
        except Exception as e:
            db.session.rollback()
            return {"error": f"Error al crear la cita: {str(e)}"}
        
    # NUEVO MÉTODO
    def obtener_citas(self):
        try:
            hoy = date.today()
            citas = Cita.query.filter(Cita.fecha >= hoy).all()

            resultado = []
            for cita in citas:
                resultado.append({
                    "idcita": cita.idcita,
                    "fkidusuario": cita.fkidusuario,
                    "fkidpsicologo": cita.fkidpsicologo,
                    "fecha": cita.fecha.strftime("%Y-%m-%d"),
                    "horainicio": cita.horainicio.strftime("%H:%M"),
                    "horafin": cita.horafin.strftime("%H:%M"),
                    "estado": cita.estado
                })

            return resultado
        except Exception as e:
            return {"error": f"Error al obtener citas: {str(e)}"}