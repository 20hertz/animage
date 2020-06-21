import os


class Config(object):
    UPLOAD_FOLDER = "/tmp"
    SECRET_KEY = os.urandom(12)


class DevelopmentConfig(Config):
    pass


class StagingConfig(Config):
    pass


class TestConfig(Config):
    pass


configs = dict(development=DevelopmentConfig, staging=StagingConfig, test=TestConfig)
