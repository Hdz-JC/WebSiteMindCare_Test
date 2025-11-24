from datetime import datetime, timedelta
from app import create_app
from app.models import db
from app.models.citas_model import Cita
from app.utils.mail_utils import send_email, generate_token
from flask import url_for

# Creamos la app ya configurada
app = create_app()
app.app_context().push()

def enviar_recordatorios():
    ahora = datetime.now()
    dentro_24h = ahora + timedelta(hours=24)

    citas = Cita.query.filter(
        Cita.fecha_hora >= ahora,
        Cita.fecha_hora <= dentro_24h,
        Cita.estado == "Pendiente",
        Cita.recordatorio_enviado == False    # EVITA DUPLICADOS
    ).all()

    for cita in citas:
        token = generate_token(f"{cita.idcita}:{cita.fkidusuario}")

        confirm_url = url_for("mail_bp.confirmar", id_cita=cita.idcita, token=token, _external=True)
        cancel_url = url_for("mail_bp.cancelar", id_cita=cita.idcita, token=token, _external=True)

        send_email(
            subject="Recordatorio de cita",
            recipients=[cita.usuario.email],   # <- AJÚSTALO según tu relación
            template_name="recordatorio",
            fecha=cita.fecha,
            hora=cita.horainicio,
            confirm_url=confirm_url,
            cancel_url=cancel_url
        )

        cita.enviorecordatorio = True
        cita.fecharecordatorio = datetime.now()
        db.session.commit()


if __name__ == "__main__":
    enviar_recordatorios()