import os


class Config(object):
    """Base config class """
    DEBUG = False
    SECRET_KEY = os.getenv("SECRET_KEY")


class Development(Config):
    """The configurations for development """
    DEBUG = True
    TESTING = False
    APP_SETTINGS = "development"
    ENV = "development"


class Testing(Config):
    """ The configurations for testing """
    TESTING = True
    DEBUG = True
    APP_SETTINGS = "testing"
    ENV = "testing"


class Production(Config):
    """The configurations for production environtment"""
    DEBUG = False
    TESTING = False
    APP_SETTINGS = "production"
    ENV = "production"


configurations = {
    "development": Development,
    "testing": Testing,
    "production": Production
}
