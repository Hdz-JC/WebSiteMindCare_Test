from datetime import datetime, timedelta
from flask import url_for
from app.models import db
from app.models.citas_model import Cita
from app.utils.mail_utils import send_email, generate_token
import os
from dotenv import load_dotenv

# Esta función recibe 'app' como argumento para poder usar la base de datos
def ejecutar_envio_recordatorios(app):
    load_dotenv()
    # 1. Hacemos el truco: Definimos el servidor MANUALMENTE solo para este momento
    # Esto simula que hay una petición web real
    host_para_correos = os.getenv('DOMAIN_URL') # Lee la variable nueva o usa localhost
    
    # Limpiamos http:// si viene sucio
    host_para_correos = host_para_correos.replace('http://', '').replace('https://', '')
   
    with app.app_context():
        app.config['SERVER_NAME'] = host_para_correos
        app.config['PREFERRED_URL_SCHEME'] = 'http'
        
        print(f"--- Ejecutando tarea automática: {datetime.now()} ---")
        
        ahora = datetime.now()
        dentro_24h = ahora + timedelta(hours=24)

        citas = Cita.query.filter(
            Cita.fecha >= ahora,
            Cita.fecha <= dentro_24h,
            Cita.estado == "pendiente",
            Cita.enviorecordatorio == False
        ).all()

        if not citas:
            print("-> No hay citas pendientes de recordatorio.")
            return

        for cita in citas:
            try:
                # Generamos el token y las URLs
                token = generate_token(f"{cita.idcita}:{cita.fkidusuario}")
                
                confirm_url = url_for("mail_bp.confirmar", idcita=cita.idcita, token=token, _external=True)
                cancel_url = url_for("mail_bp.cancelar", idcita=cita.idcita, token=token, _external=True)

                # Enviamos el correo
                send_email(
                    subject="Recordatorio de cita - MindCare",
                    recipients=[cita.usuario.email],
                    template_name="recordatorio",
                    fecha=cita.fecha,
                    horainicio=cita.horainicio,
                    confirm_url=confirm_url,
                    cancel_url=cancel_url
                )

                # Actualizamos la BD
                cita.enviorecordatorio = True
                cita.fecharecordatorio = datetime.now()
                db.session.commit()
                print(f"-> Correo enviado para cita {cita.idcita}")

            except Exception as e:
                print(f"Error en cita {cita.idcita}: {e}")
                db.session.rollback()