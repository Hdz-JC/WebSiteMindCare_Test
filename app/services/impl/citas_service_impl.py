from app.models.citas_model import Cita
from app.models.user_model import User
from app.models import db
from app.services.citas_service_interface import CitaService
from datetime import date,datetime
from sqlalchemy import text

class CitaServiceImpl(CitaService):
    
    def agendar_cita(self, data):
        try:
            psicologo = User.query.filter_by(rol='psicologo').first()
            if not psicologo:
                return {"error": "No hay psicólogo registrado en el sistema"}

            hoy = date.today()
            fecha_cita = datetime.strptime(data["fecha"], "%Y-%m-%d").date()

            # --- VALIDACIÓN DE DÍA BLOQUEADO (NUEVO) ---
            # Buscamos si existe una cita donde el usuario sea el mismo psicólogo en esa fecha
            dia_inhabil = Cita.query.filter(
                Cita.fkidpsicologo == psicologo.id,
                Cita.fkidusuario == psicologo.id, # Clave: El psicólogo es su propio paciente
                Cita.fecha == fecha_cita,
                Cita.estado != 'cancelada'        # Solo si el bloqueo está activo
            ).first()

            if dia_inhabil:
                # Si encontramos el bloqueo, rechazamos la petición y devolvemos error
                return {"error": "Lo sentimos, el psicólogo no labora el día seleccionado."}
            # -------------------------------------------

            # Si la cita es hoy, cambia estado a 'aceptada', si no, 'pendiente'
            estado_cita = "aceptada" if fecha_cita == hoy else "pendiente"

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

    #Metodo de Historial
    def obtener_historial(self, user_id):
        query = text("""
            SELECT
                c.idcita,
                c.fecha,
                c.horainicio,
                c.horafin,
                c.estado,
                c.descripcioncancelado,
                u.id AS usuario_id,
                CONCAT(u.nombre, ' ', u.paterno, ' ', COALESCE(u.materno, '')) AS usuario_nombre,
                p.id AS psicologo_id,
                CONCAT(p.nombre, ' ', p.paterno, ' ', COALESCE(p.materno, '')) AS psicologo_nombre
            FROM citas c
            JOIN usuarios u ON u.id = c.fkidusuario
            JOIN usuarios p ON p.id = c.fkidpsicologo
            WHERE u.id = :user_id
            ORDER BY c.fecha, c.horainicio
        """)

        result = db.session.execute(query, {"user_id": user_id})
        return [dict(row._mapping) for row in result]

def obtener_historial(self, user_id):
    try:
        citas = Cita.query.filter_by(fkidusuario=user_id).order_by(Cita.fecha.desc()).all()
        resultado = []
        for cita in citas:
            resultado.append({
                "idcita": cita.idcita,
                "fecha": cita.fecha.strftime("%Y-%m-%d"),
                "horainicio": cita.horainicio.strftime("%H:%M"),
                "horafin": cita.horafin.strftime("%H:%M"),
                "estado": cita.estado
            })
        return resultado
    except Exception as e:
        return {"error": f"Error al obtener historial: {str(e)}"}
