from app import db
from datetime import datetime
from app.utils.security import hash_password

class User(db.Model):
  __tablename__ = 'usuarios'
  id = db.Column(db.Integer, primary_key=True)
  paterno = db.Column(db.String(15), nullable=False)
  materno = db.Column(db.String(15))
  nombre = db.Column(db.String(30), nullable=False)
  fecha_nacimiento = db.Column(db.Date, nullable=True)
  sexo = db.Column(db.String(1), nullable=True)
  direccion = db.Column(db.String(60), nullable=True)
  celular = db.Column(db.String(10), nullable=True)
  email = db.Column(db.String(254), unique=True, nullable=False)
  password = db.Column(db.String(128), nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.utcnow)

  @staticmethod
  def create(paterno, materno, nombre, fecha_nacimiento, sexo, direccion, celular, email, password):
    hashed = hash_password(password)
    user = User(
      paterno=paterno,
      materno=materno,
      nombre=nombre,
      fecha_nacimiento=fecha_nacimiento,
      sexo=sexo,
      direccion=direccion,
      celular=celular,
      email=email,
      password=hashed
    )
    db.session.add(user)
    db.session.commit()
    return user
