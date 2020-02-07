import logging
import logging.handlers as handlers
import configparser
import os
import time
# from pympler import asizeof
# import dis


class SetupAll:
    __slots__ = ('file_name')

    def __init__(self, file_name, rotate_on):
        self.file_name = file_name
        self.rotate_on = rotate_on

    def setup_config(self):
        config = configparser.ConfigParser()
        BASE_DIR = os.path.dirname(__file__)
        config_file = os.path.join(BASE_DIR, self.file_name)
        config.read(config_file)
        return config

    def config_logging(self, LOG, LOG_LEVEL_ON):
        if self.setup_config().get(LOG, LOG_LEVEL_ON) == "True":
            return True
        else:
            return False

    def out_console(self):
        if self.setup_config().get("CONSOLE", "OUTPUT_IN_CONSOLE") == "True":
            return True
        else:
            return False

    def setup_log(self):
        logger = logging.getLogger("server_loggerp")
        file_name = self.setup_config().get("FILE", "LOG_FILE")
        BASE_DIR = os.path.dirname(__file__)
        log_file = os.path.join(BASE_DIR, file_name)
        fh = logging.FileHandler(log_file)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        if self.out_console():
            console = logging.StreamHandler()
            console.setFormatter(formatter)
            logger.addHandler(console)
        if self.rotate_on:
            file_rotate = handlers.TimedRotatingFileHandler(file_name, when='D', interval=1, backupCount=10)
            logger.addHandler(file_rotate)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        return logger


class LogLevel(SetupAll):
    __slots__ = ('file_name', 'rotate_on', 'set_log')

    def __init__(self, file_name, rotate_on: bool):
        # self.file_name = file_name
        # self.rotate_on = rotate_on
        super(LogLevel, self).__init__(file_name=file_name, rotate_on=rotate_on)
        self.set_log = self.setup_log()

    def info_log(self, msg):
        if not self.config_logging("INFO", "INFO_LEVEL_ON"):
            logging.disable(logging.INFO)
        else:
            self.set_log.setLevel(logging.INFO)
            self.set_log.info(msg)

    def debug_log(self, msg):
        if not self.config_logging("DEBUG", "DEBUG_LEVEL_ON"):
            logging.disable(logging.DEBUG)
        else:
            self.set_log.setLevel(logging.DEBUG)
            self.set_log.debug(msg)

    def warning_log(self, msg):
        if not self.config_logging("WARNING", "WARNING_LEVEL_ON"):
            logging.disable(logging.WARNING)
        else:
            self.set_log.setLevel(logging.WARNING)
            self.set_log.warning(msg)

    def error_log(self, msg):
        if not self.config_logging("ERROR", "ERROR_LEVEL_ON"):
            logging.disable(logging.ERROR)
        else:
            self.set_log.setLevel(logging.ERROR)
            self.set_log.error(msg)

    def critical_log(self, msg):
        if not self.config_logging("CRITICAL", "CRITICAL_LEVEL_ON"):
            logging.disable(logging.CRITICAL)
        else:
            self.set_log.setLevel(logging.CRITICAL)
            self.set_log.critical(msg)


if __name__ == "__main__":
    logg = LogLevel(file_name="config_logg.ini", rotate_on=False)
    # print(asizeof.asizeof(logg))
    # dis.dis(logg.info_log)

    while 1:
        time.sleep(20)
        logg.info_log("INFO")
        logg.debug_log("DEBUG")
        logg.error_log("ERROR")
        logg.warning_log("WARNING")
        logg.warning_log("CRITICAL")
