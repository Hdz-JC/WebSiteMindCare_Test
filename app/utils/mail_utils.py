from flask_mail import Message
from flask import current_app
from threading import Thread
from itsdangerous import URLSafeTimedSerializer
import os
from app import mail


# ----------------------------
# ENVÍO ASÍNCRONO DE CORREOS
# ----------------------------
def send_async_email(app, msg):
    """Función que envía el correo dentro del contexto de Flask"""
    with app.app_context():
        mail.send(msg)


def send_email(subject, recipients, template_name, **context):
    """
    Envía un correo usando plantilla HTML (y .txt opcional).
    Las plantillas deben estar en /templates/emails/
    """
    app = current_app._get_current_object()

    msg = Message(subject, recipients=recipients)

    # Renderizado de plantilla HTML
    msg.html = app.jinja_env.get_template(
        f"emails/{template_name}.html"
    ).render(**context)

    # Fallback para texto plano (si existe)
    try:
        msg.body = app.jinja_env.get_template(
            f"emails/{template_name}.txt"
        ).render(**context)
    except:
        msg.body = ""

    # Hilo para no bloquear Flask
    thr = Thread(target=send_async_email, args=(app, msg))
    thr.start()
    return thr


# ----------------------------
# TOKENS PARA CONFIRMAR/CANCELAR
# ----------------------------
def _serializer():
    secret = os.getenv("SECRET_KEY", "default-secret-key")
    return URLSafeTimedSerializer(secret)


def generate_token(data):
    return _serializer().dumps(data)


def confirm_token(token, expiration=86400):  # 24 horas
    try:
        return _serializer().loads(token, max_age=expiration)
    except:
        return None