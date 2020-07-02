import os


class BaseConfig(object):
    UPLOAD_FOLDER = "/tmp"
    SECRET_KEY = os.urandom(12)


class DevelopmentConfig(BaseConfig):
    pass


class StagingConfig(BaseConfig):
    pass


config_by_name = dict(development=DevelopmentConfig, staging=StagingConfig)
