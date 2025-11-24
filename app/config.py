import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://user_postgres:password_postgres@localhost:5433/db_postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'mind_care_project'
    # Configuración de Flask-Mail
    MAIL_SERVER = 'smtp.sendgrid.net'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'apikey'     
    MAIL_PASSWORD = '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' 
    MAIL_DEFAULT_SENDER = ('MindCare', 'angel_jair.00@hotmail.com')