import os


class Config(object):
    DEBUG = False
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_BACKEND_URL = os.environ.get('CELERY_BACKEND_URL', 'redis://localhost:6379/0')
    CELERY_ALWAYS_EAGER = False #Run celery tasks synchronously
    API_BASE = "https://the-one-api.dev"


class ProductionConfig(Config):
    DEBUG = False
    ENV = 'production'


class StageConfig(Config):
    DEBUG = False
    ENV = 'stage'


class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'
    CELERY_ALWAYS_EAGER = True #Run celery tasks synchronously


class TestingConfig(Config):
    DEBUG = True
    ENV = 'test'
