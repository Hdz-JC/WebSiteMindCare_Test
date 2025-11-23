from app.services.notas_service_interface import NotasService
from app.models import db, NotaCita,Cita,Expediente
from datetime import datetime, timezone

class NotasServiceImpl(NotasService):
    def agregar_nota(self, idcita, contenido, user, titulo):
        rol = user.rol.value if hasattr(user.rol, "value") else user.rol
        if rol.lower() != "psicologo":
            raise PermissionError("No autorizado")

        cita = Cita.query.filter_by(idcita=idcita).first()
        if not cita:
            raise Exception("La cita no existe")

        paciente_id = cita.fkidusuario
        expediente = Expediente.query.filter_by(fkidusuario=paciente_id).first()

        if not expediente:
            expediente = Expediente(fkidusuario=paciente_id)
            db.session.add(expediente)
            db.session.commit()

        # Crear la nota con título y contenido
        nota = NotaCita(
            titulo=titulo,
            descripcionnota=contenido,
            fechanota=datetime.now(timezone.utc),
            fkidexpediente=expediente.idexpediente
        )
        db.session.add(nota)
        db.session.commit()

    def obtener_notas_por_usuario(self, user_id):
            # Traer el expediente del paciente
            expediente = Expediente.query.filter_by(fkidusuario=user_id).first()
            if not expediente:
                return []

            # Traer todas las notas del expediente
            notas = NotaCita.query.filter_by(fkidexpediente=expediente.idexpediente)\
                                .order_by(NotaCita.fechanota.desc())\
                                .all()

            if not notas:
                return []

            # Traer info del usuario
            user = expediente.usuario

            resultado = []
            for nota in notas:
                resultado.append({
                    "idNota": nota.idnota,
                    "contenido": nota.descripcionnota,
                    "fecha": nota.fechanota.strftime("%Y-%m-%d %H:%M"),
                    "autor": f"{user.nombre} {user.paterno}"
                })

            return resultado

