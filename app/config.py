import os
from dotenv import load_dotenv

if not os.environ.get('DATABASE_URL'):
    load_dotenv()

class Config:

    # Intentamos obtener la URL de Docker primero
    uri = os.environ.get('DATABASE_URL')

    # Si uri existe y empieza con "postgres://", SQLAlchemy moderno prefiere "postgresql://"
    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = uri or 'postgresql://user_postgres:password_postgres@localhost:5433/db_postgres'
    if not SQLALCHEMY_DATABASE_URI:
        # Fallback para desarrollo local si no hay .env ni Docker
        SQLALCHEMY_DATABASE_URI = 'postgresql://user_postgres:password_postgres@localhost:5433/db_postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
 
   
    # Configuración de Correo
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    _sender_name = os.environ.get('MAIL_DEFAULT_SENDER_NAME')
    _sender_email = os.environ.get('MAIL_DEFAULT_SENDER_EMAIL')
    MAIL_DEFAULT_SENDER = (_sender_name, _sender_email)

    # Seguridad
    SECRET_KEY=os.getenv('SECRET_KEY')

    # Configuración del Server (Para que funcione el scheduler)
    SERVER_NAME=None
    '''
    # Configuración de Flask-Mail
    MAIL_SERVER = 'MAIL_SERVER'
    MAIL_PORT = 'MAIL_PORT'
    MAIL_USE_TLS = 'MAIL_USE_TLS'
    MAIL_USERNAME = 'MAIL_USERNAME'     
    MAIL_PASSWORD = 'MAIL_PASSWORD' 
    MAIL_DEFAULT_SENDER = 'MAIL_DEFAULT_SENDER'
    '''
