import os

class Config:
    # Configuración de la base de datos
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #     'mysql+mysqlconnector://root:root@localhost/cac_movies'
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+mysqlconnector://root:Matilda.2023@localhost/cac_movies'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Clave secreta para sesiones y flash messages
    SECRET_KEY = 'tu_secreto'
