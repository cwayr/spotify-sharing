import os


class Config(object):
    """Parent configuration class."""

    DEBUG = False
    SECRET = os.getenv("SECRET") or 'secret'


class developmentConfig(Config):
    """Configurations for development."""

    DEBUG = True
    DATABASE_URL = os.environ.get('DEV_DATABASE_URL')
    ENV= 'development'

class TestingConfig(Config):
    """Configurations for testing."""

    TESTING = True
    DEBUG = True
    DATABASE_URL = os.environ.get('TEST_DATABASE_URL')
    ENV = 'testing'

class ProductionConfig(Config):
    """Configurations for production."""

    DEBUG = False
    DATABASE_URL = os.environ.get('DATABASE_URL')
    ENV = 'production'

app_config = {
    'DEFAULT': developmentConfig,
    'TESTING': TestingConfig,
    'PRODUCTION': ProductionConfig
}