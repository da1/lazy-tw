import ConfigParser

class Config:
    """ twitter config """
    __HOME_PATH="$PROJECT_PATH/lazy/"
    __FILE_NAME = "tw/config.ini"
    def __init__(self):
        conf = ConfigParser.SafeConfigParser()
        conf.read(self.__HOME_PATH + self.__FILE_NAME)
        self.__CONSUMER_KEY    = conf.get("config", "consumer_key")
        self.__CONSUMER_SECRET = conf.get("config", "consumer_secret")
        self.__CALLBACK_URL    = conf.get("config", "callback_url")
        self.__LAZY_START      = int(conf.get("config", "lazy_start"))
        self.__LAZY_END        = int(conf.get("config", "lazy_end"))

    @property
    def CONSUMER_KEY(self):
        return self.__CONSUMER_KEY

    @property
    def CONSUMER_SECRET(self):
        return self.__CONSUMER_SECRET

    @property
    def CALLBACK_URL(self):
        return self.__CALLBACK_URL

    @property
    def LAZY(self):
        return (self.__LAZY_START, self.__LAZY_END)
