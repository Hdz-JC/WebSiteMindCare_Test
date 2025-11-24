from flask import Blueprint, render_template, url_for
from app.models.citas_model import Cita
from app.models import db
from app.utils.mail_utils import send_email, generate_token, confirm_token

mail_bp = Blueprint("mail_bp", __name__)


# --------------------------------------
# ENVIAR CORREO DE PRUEBA MANUAL
# --------------------------------------
@mail_bp.route("/test_mail/<int:idcita>")
def test_mail(idcita):
    cita = Cita.query.get_or_404(idcita)

    # Datos para token (id + id de usuario)
    data = f"{cita.idcita}:{cita.fkidusuario}"
    token = generate_token(data)

    # Links de confirmación/cancelación
    confirm_url = url_for(
        "mail_bp.confirmar", idcita=cita.idcita, token=token, _external=True
    )
    cancel_url = url_for(
        "mail_bp.cancelar", idcita=cita.idcita, token=token, _external=True
    )

    # Debes ajustar cita.usuario.correo según tu modelo real
    if cita.usuario is None:
        return "Error: Esta cita no tiene un usuario asignado."
    correo_paciente = cita.usuario.email


    send_email(
        subject="Recordatorio de tu cita - MindCare",
        recipients=[correo_paciente],
        template_name="recordatorio",
        fecha=cita.fecha,
        horainicio=cita.horainicio,
        confirm_url=confirm_url,
        cancel_url=cancel_url
    )

    return "Correo de prueba enviado."


# --------------------------------------
# CONFIRMAR CITA
# --------------------------------------
@mail_bp.route("/confirmar/<int:idcita>/<token>")
def confirmar(idcita, token):
    data = confirm_token(token)
    if not data:
        return "El enlace ha expirado o es inválido."

    token_id, _ = data.split(":")

    if str(idcita) != token_id:
        return "El token no corresponde a esta cita."

    cita = Cita.query.get_or_404(idcita)
    cita.estado = "aceptada"
    db.session.commit()

    return render_template("emails/confirmacion.html", cita=cita)


# --------------------------------------
# CANCELAR CITA
# --------------------------------------
@mail_bp.route("/cancelar/<int:idcita>/<token>")
def cancelar(idcita, token):
    data = confirm_token(token)
    if not data:
        return "El enlace ha expirado o es inválido."

    token_id, _ = data.split(":")

    if str(idcita) != token_id:
        return "El token no corresponde a esta cita."

    cita = Cita.query.get_or_404(idcita)
    cita.estado = "cancelada"
    db.session.commit()

    return render_template("emails/cancelacion.html", cita=cita)
