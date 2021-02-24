class Config:

    DEBUG = True

    SQLALCHEMY_DATABASE_URL = 'postgresql+psycopg2://YOURURL'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = 'Your secret key'

    JWT_ERROR_MESSAGE_KEY = 'message'

    JWT_BLACKLIST_ENABLE = True

    JWT_BLACKLIST_TOKEN_CHECK = ['access', 'refresh']
