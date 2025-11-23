from flask import Flask, g, session
from .config import Config
from app.models import db
from app.models.user_model import User  # Importa tu modelo

def create_app():
    app = Flask(__name__) 
    app.config.from_object(Config)
    db.init_app(app)

    # --- Rutas / Blueprints ---
    from .controllers.public.user_routes import user_bp
    app.register_blueprint(user_bp)

    from .controllers.public.citas_routes import citas_bp
    app.register_blueprint(citas_bp)

    # Registro de blueprints
    from .controllers.public.psicologo_routes import psicologo_bp
    app.register_blueprint(psicologo_bp)

    from .controllers.public.notas_routes import notas_bp
    app.register_blueprint(notas_bp)


    # --- Before request: cargar usuario logueado ---
    @app.before_request
    def load_logged_in_user():
        user_id = session.get('user_id')
        if user_id is None:
            g.user = None
        else:
            g.user = User.query.get(user_id)

    return app