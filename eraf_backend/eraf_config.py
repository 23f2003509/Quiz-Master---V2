
from datetime import timedelta
from flask_caching import Cache

cache = Cache()
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

    CACHE_TYPE = 'redis'
    CACHE_REDIS_HOST = 'localhost'
    CACHE_REDIS_PORT = 6379 
    CACHE_REDIS_DB = 0 
    CACHE_REDIS_URL = 'redis://localhost:6379'

    CACHE_DEFAULT_TIMEOUT = 300 

    MAIL_SERVER = 'localhost'            
    MAIL_PORT = 1025                    
    MAIL_USE_TLS = False                
    MAIL_USERNAME = 'admin@gmail.com' 
    MAIL_PASSWORD = 'admin'
    MAIL_DEFAULT_SENDER = 'admin@gmail.com'


