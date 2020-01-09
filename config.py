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
    PORT_APP = 8443
    MAIL_USE_TLS = True
    # Включение защиты против "Cross-site Request Forgery (CSRF)"
    CSRF_ENABLED = True
    SECRET_KEY = 'YOUR_RANDOM_SECRET_KEY'
    def __init__(self):
        super().__init__("config.ini")
    # Определяет, включен ли режим отладки
    # В случае если включен, flask будет показывать
    # подробную отладочную информацию. Если выключен -
    # - 500 ошибку без какой либо дополнительной информации.
        self.API_KEY_TG = self.read_config("API_KEY", "API_KEY_TG")
        self.API_KEY_DIALOG = self.read_config("API_KEY", "API_KEY_DIALOG")
        self.API_KEY_WEATHER = self.read_config("API_KEY", "API_KEY_WEATHER")
        self.IP_LAMP = self.read_config("IP", "IP_LAMP")
        self.IP_BROKER = self.read_config("IP", "IP_BROKER")
        DB_NAME = self.read_config("DB_SETTING", "DB_NAME")
        USER_DB = self.read_config("DB_SETTING", "USER_DB")
        PASSWORD = self.read_config("DB_SETTING", "PASSWORD")
        HOST = self.read_config("DB_SETTING", "HOST")
        self.PORT = self.read_config("DB_SETTING", "PORT")
        self.USER_BROKER = self.read_config("MQTT_BROKER", "USER_BROKER")
        self.PASSWORD_BROKER = self.read_config("MQTT_BROKER", "PASSWORD_BROKER")
        self.SQLALCHEMY_DATABASE_URI = f'postgresql://{USER_DB}:{PASSWORD}@{HOST}/{DB_NAME}'
        self.SQLALCHEMY_TRACK_MODIFICATIONS = True
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