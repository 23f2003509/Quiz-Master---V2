

from datetime import timedelta



class Config():
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class localDevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///eraf_database.db'
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_PASSWORD_SALT = 'ERAF_mad2_propject-on-qyuizamasteer is the best'
    JWT_SECRET_KEY = 'ERAF_mad2_propject-on-qyuizamasteer is the best'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)