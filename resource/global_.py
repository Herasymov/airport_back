import logging
import os
import time
from datetime import datetime

class Profiler(object):
    def __enter__(self):
        self._startTime = time.time()

    def __exit__(self, type, value, traceback):
        print ("Elapsed time: {:.6f} sec".format(time.time() - self._startTime))


class LoggerSetup:
    def __init__(self, path: str, name="default"):
        path = f"{path}/logs"
        print(path)

        os.makedirs(path, exist_ok=True)

        logging_ = logging.getLogger()
        logging_.setLevel(logging.DEBUG)  # TODO change this param for PROD
        logging_.addHandler(logging.FileHandler(f"{path}/{datetime.now()}.{name}.log", mode='w'))


class RedisSettings:
    def  __init__(self, host: str, port: int, db: int, encoding:str='utf-8'):
        assert type(host) == str
        assert type(port) == int
        assert type(db) == int
        assert type(encoding) == str

        self.host = host
        self.port = port
        self.db = db
        self.encoding = encoding


class McacheSettings:
    def __init__(self, host: str, port: int):
        assert type(host) == str
        assert type(port) == int

        self.host = host
        self.port = port


class PostgreSettings:
    def __init__(self, host: str, port: str, password: str, dbname: str, user: str):
        assert type(host) == str
        assert type(port) == str
        assert type(password) == str
        assert type(dbname) == str
        assert type(user) == str

        self.host = host
        self.port = port
        self.password = password
        self.dbname = dbname
        self.user = user


class JwtSettings:
    def __init__(self, key: str, algorithm: str = 'HS256'):
        assert type(key) == str
        assert type(algorithm) == str

        self.key = key
        self.algorithm = algorithm


class rabbitMqSetting:
    def __init__(self, port: int, url: str, exchange_name: str):
        assert type(port) == int
        assert type(url) == str
        assert type(exchange_name) == str

        self.port = port
        self.url = url
        self.exchangeName = exchange_name


class MongoDbSetting:
    def __init__(self, host: str, port: int, user: str, password: str):
        assert type(port) == int
        assert type(host) == str
        assert type(user) == str
        assert type(password) == str

        # TODO find config
        self.url = "mongodb://localhost:27018"
        # self.url = f"mongodb://{user}:{password}@{host}:{port}/auto_parts"
        self.database = 'auto_parts'

        self.seller_push_collection = 'seller_push'
        self.customer_push_collection = 'customer_push'


class MailSetting:
    def __init__(self, from_: str, login: str, password: str, url: str, port: int, authentication: str='plain'):
        assert type(from_) == str
        assert type(login) == str
        assert type(password) == str
        assert type(url) == str
        assert type(port) == int
        assert type(authentication) == str

        self.from_ = from_
        self.login = login
        self.password = password
        self.url = url
        self.port = port
        self.authentication = authentication


class GlobalConfig:
    def __init__(self):
        self.mongoDbSettings = MongoDbSetting(
            host="localhost",
            port=27017,
            user="root",
            password="root"
        )

        self.redisSessionKey = RedisSettings(
            host="127.0.0.1",
            port=6379,
            db=5
        )

        self.redisSids = RedisSettings(
            host="127.0.0.1",
            port=6379,
            db=6
        )

        self.mcacheSettings = McacheSettings(host="localhost", port=11211)

        self.postgreSettings = PostgreSettings(
            user='myusername',
            dbname='feelo4',
            password='root',
            host='localhost',
            port='5432'
        )

        self.jwtApiMobileSeller = JwtSettings(key="FB0F43D30719DDDA03BE708E4D7585B1")
        self.jwtApiMobileCustomer = JwtSettings(key="FB0F43D30719DDDA03BE708E4D7585B2")
        self.jwtApiAdmin = JwtSettings(key="1745903B0195BB52DB493BEB6FA59176")

        self.rabbitMqSetting = rabbitMqSetting(
            port=5672,
            url="amqp://guest:guest@localhost/",
            exchange_name="autoparts"
        )

        self.mailSetting = MailSetting(
            from_="peregovorka@brander.ua",
            login="brander_peregovorka",
            password="ab8d49f4d90d75f73",
            url='52.47.122.250',
            port=25
        )

        self.MAX_FILE_SIZE = 1024 * 10
