from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user_model import User
from .citas_model import Cita
from .notascita_model import NotaCita
from .expediente_model import Expediente


