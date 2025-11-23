from app.models import db

class Expediente(db.Model):
    __tablename__ = 'expediente'

    idexpediente = db.Column(db.Integer, primary_key=True)

    fkidusuario = db.Column(
        db.Integer, 
        db.ForeignKey('usuarios.id'), 
        unique=True, 
        nullable=False
    )
    # Relaciones
    usuario = db.relationship("User", back_populates="expediente")
    nota = db.relationship("NotaCita", back_populates="expediente")
