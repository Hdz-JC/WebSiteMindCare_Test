import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://user_postgres:password_postgres@localhost:5433/db_postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'mind_care_project'