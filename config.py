import os

class Config:
    SECRET_KEY = 'clave_secreta_proyecto_bd'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:admin123@localhost/db_proyecto1'
    SQLALCHEMY_TRACK_MODIFICATIONS = False