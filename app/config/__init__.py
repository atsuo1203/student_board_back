import os


class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = \
        'mysql+pymysql://{user}:{password}@{host}/student_board?charset=utf8' \
        .format(**{
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', ''),
            'host': os.getenv('DB_HOST', 'localhost'),
        })
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    JSON_AS_ASCII = False


Config = DevelopmentConfig
