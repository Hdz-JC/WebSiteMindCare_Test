'''
from app import db
#from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.config import Config
from app.utils.security import hash_password

# Crear el motor de la base de datos
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

#Base de automapeo
Base = automap_base()

#Reflejar la base de datos existente
Base.prepare(engine,reflect=True)

User = Base.classes.users

def create_user(id,paterno,materno,nombre,fecha_nacimiento,sexo,direccion,celular,email,password):
    new_user = User(
      id=id,
      paterno=paterno,
      materno=materno,
      nombre=nombre,
      fecha_nacimiento=fecha_nacimiento,
      sexo=sexo,
      direccion=direccion,
      celular=celular,
      email=email,
      password = hash_password(password)  
    )
    session.add(new_user)
    session.commit()
    return new_user


class User(db.Model):
    
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    paterno = db.Column(db.String(50),nullable=False)
    materno = db.Column(db.String(50))
    nombre = db.Column(db.String(50), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    sexo = db.Column(db.Char, nullable=False)
    direccion = db.Column(db.String,nullable=False)
    celular = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
'''
