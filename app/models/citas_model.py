from app.models import db
from datetime import datetime
from sqlalchemy import Enum
import enum


class EstadoCitaEnum(enum.Enum):
    aceptada = "aceptada"
    pendiente = "pendiente"
    cancelada = "cancelada"
    finalizada = "finalizada"

class Cita(db.Model):
    __tablename__ = 'citas'

    idcita = db.Column(db.Integer, primary_key=True)
    fkidusuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    fkidpsicologo = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    fecha = db.Column(db.Date, nullable=False)
    estado = db.Column(db.String(20), default='pendiente', nullable=False)
    horainicio = db.Column(db.Time, nullable=False)
    horafin = db.Column(db.Time, nullable=False)
    
    enviorecordatorio = db.Column(db.Boolean, default=False)
    fecharecordatorio = db.Column(db.DateTime)
    descripcioncancelado = db.Column(db.String(255))

    # RELACIONES ---------------------------
    usuario = db.relationship(
        "User",
        foreign_keys=[fkidusuario],
        backref="citas_paciente"
    )

    psicologo = db.relationship(
        "User",
        foreign_keys=[fkidpsicologo],
        backref="citas_psicologo"
    )

    