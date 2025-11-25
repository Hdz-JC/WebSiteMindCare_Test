from flask import Flask, g, session
from .config import Config
from flask_mail import Mail
from flask_apscheduler import APScheduler
from app.models import db
import os
from dotenv import load_dotenv

load_dotenv()

from app.models.user_model import User 


mail=Mail()


def create_app():
    app = Flask(__name__) 
    app.config.from_object(Config)
    db.init_app(app)
    mail.init_app(app)

    # --- AGREGA ESTO ---
    # Esto le dice a Flask: "Cuando generes links en segundo plano, usa esta dirección"
    #app.config['SERVER_NAME'] = os.getenv('SERVER_NAME') 
    #app.config['APPLICATION_ROOT'] = '/' 
    #app.config['PREFERRED_URL_SCHEME'] = 'http'

    # 2. Inicializar el Scheduler
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()

    # 3. Definir la tarea programada
    # 'interval' indica que se repite. 'seconds', 'minutes' o 'hours'.
    @scheduler.task('interval', id='tarea_recordatorios', seconds=10)
    def tarea_programada():
        from app.tasks import ejecutar_envio_recordatorios
        # Pasamos la app actual a la función para que tenga contexto de BD
        ejecutar_envio_recordatorios(app)

    # --- Rutas / Blueprints ---
    from app.routes.user_routes import user_bp
    app.register_blueprint(user_bp)

    from app.routes.citas_routes import citas_bp
    app.register_blueprint(citas_bp)

    # Registro de blueprints
    from app.routes.psicologo_routes import psicologo_bp
    app.register_blueprint(psicologo_bp)

    from app.routes.notas_routes import notas_bp
    app.register_blueprint(notas_bp)

    from app.routes.mail_routes import mail_bp
    app.register_blueprint(mail_bp)

    from app.routes.monitor_routes import monitor_bp
    app.register_blueprint(monitor_bp)



    # --- Before request: cargar usuario logueado ---
    @app.before_request
    def load_logged_in_user():
        user_id = session.get('user_id')
        if user_id is None:
            g.user = None
        else:
            g.user = User.query.get(user_id)

    return app