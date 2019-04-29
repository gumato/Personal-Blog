import os

class Config:
    '''
    General configuration parent class
    '''
    SQLALCHEMY_DATABASE_URL = 'postgresql+psycopg2://pricilla:gume@localhost/blog'



class ProdConfig(Config):
    '''
    Production  configuration child class

    Args:
        Config: The parent configuration class with General configuration settings
    '''
    pass


class DevConfig(Config):
    '''
    Development  configuration child class

    Args:
        Config: The parent configuration class with General configuration settings
    '''

    DEBUG = True
