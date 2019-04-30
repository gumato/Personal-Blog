import os

class Config:
    '''
    General configuration parent class
    '''
    SECRET_KEY = 'gumeshi1'
    # SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://pricilla:1234@localhost/bolg'
    UPLOADED_PHOTOS_DEST ='app/static/photos'

    # email configurations
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    # SUBJECT_PREFIX = 'Personal Blog'
    # SENDER_EMAIL = 'gumatopricilla22@gmail.com'

    # simple mde  configurations
    SIMPLEMDE_JS_IIFE = True
    SIMPLEMDE_USE_CDN = True

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://pricilla:1234@localhost/blog_test'

class ProdConfig(Config):
    '''
    Production  configuration child class
    Args:
        Config: The parent configuration class with General configuration settings
    '''
    pass
    # SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")

class DevConfig(Config):
    '''
    Development  configuration child class
    Args:
        Config: The parent configuration class with General configuration settings
    '''
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://pricilla:1234@localhost/pitch'


    DEBUG = True

config_options = {
       'development':DevConfig,
       'production':ProdConfig,
       'test':TestConfig
}

