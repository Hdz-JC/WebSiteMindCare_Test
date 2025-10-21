import os

class Config:
    #SQLALCHEMY_DATABASE_URI = 'postgresql://test_user:test_password@localhost:5432/test_db'
    SQLALCHEMY_DATABASE_URI = 'postgresql://user_postgres:password_postgres@localhost:5432/db_postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'mind_care_project'