import config


class TestConfig(config.Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    # APPLICATION_ROOT = ""
    # SERVER_NAME = "localhost"