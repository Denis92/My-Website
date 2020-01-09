import configparser
import os


class ConfigReader(object):

    def __init__(self, file_name):
        self.file_name = file_name

    def read_config(self, section, option):
        config = configparser.ConfigParser()
        BASE_DIR = os.path.dirname(__file__)
        config_file = os.path.join(BASE_DIR, self.file_name)
        config.read(config_file, encoding='utf-8')
        res = config.get(section=section, option=option)
        return res


class Config(ConfigReader):
    DEBUG = True
    PORT_APP = 8043
    MAIL_USE_TLS = True
    # Включение защиты против "Cross-site Request Forgery (CSRF)"
    CSRF_ENABLED = True
    SECRET_KEY = 'YOUR_RANDOM_SECRET_KEY'
    def __init__(self):
        super().__init__("config.ini")
        self.INSTALLATION = self.read_config("INSTALLATION", "TYPE")
        self.MAIL_SERVER = self.read_config("MAIL", "MAIL_SERVER")
        self.MAIL_PORT = self.read_config("MAIL", "MAIL_PORT")
        self.MAIL_USERNAME = self.read_config("MAIL", "MAIL_USERNAME")
        self.MAIL_DEFAULT_SENDER = self.read_config("MAIL", "MAIL_DEFAULT_SENDER")
        self.MAIL_PASSWORD = self.read_config("MAIL", "MAIL_PASSWORD")


class ProductionConfig(Config):
    DEBUG = False
    HOST = "0.0.0.0"


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    HOST = "127.0.0.1"