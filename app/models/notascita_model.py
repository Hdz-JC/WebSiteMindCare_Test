from app.models import db
from datetime import datetime,timezone

class NotaCita(db.Model):
    __tablename__ = 'notascitas'

    idnota = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(50))
    descripcionnota = db.Column(db.Text, nullable=False)
    fechanota = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    # Relación con expediente
    fkidexpediente = db.Column(db.Integer, db.ForeignKey('expediente.idexpediente'), nullable=False)
    expediente = db.relationship("Expediente", back_populates="nota", uselist=False)
