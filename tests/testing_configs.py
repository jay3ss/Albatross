import config


class TestConfig(config.Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    APPLICATION_ROOT = ""
    SERVER_NAME = "localhost.localdomain"
    WTF_CSRF_ENABLED = False
