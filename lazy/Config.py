import ConfigParser
import os

class Config:
    __FILE_NAME = "/config.ini"
    def __init__(self):
        conf = ConfigParser.SafeConfigParser()
        conf.read(os.path.dirname(__file__) + self.__FILE_NAME)
        self.__PROJECT_PATH = conf.get("config", "project_path")
        self.__HOST         = conf.get("config", "host")
        self.__SECRET_KEY   = conf.get("config", "secret_key")
        self.__DEBUG        = conf.get("config", "debug")

    @property
    def PROJECT_PATH(self):
        return self.__PROJECT_PATH

    @property
    def HOST(self):
        return self.__HOST

    @property
    def SECRET_KEY(self):
        return self.__SECRET_KEY

    @property
    def DEBUG(self):
        return self.__DEBUG
