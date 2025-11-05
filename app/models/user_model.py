from app.models import db
from datetime import datetime
from sqlalchemy import Enum
import enum

class RoleEnum(enum.Enum):
    paciente = "paciente"
    psicologo = "psicologo"
    general = "general"

class User(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    paterno = db.Column(db.String(15), nullable=False)
    materno = db.Column(db.String(15))
    nombre = db.Column(db.String(30), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=True)
    sexo = db.Column(db.String(1), nullable=True)
    direccion = db.Column(db.String(60), nullable=True)
    celular = db.Column(db.String(10), unique=True, nullable=False)
    email = db.Column(db.String(254), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    rol = db.Column(db.Enum(RoleEnum), default=RoleEnum.paciente, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

