import os
from logging.handlers import RotatingFileHandler
import logging
from abc import abstractmethod, ABC

from basic_config import (
    VIEW_BASE_URL,
    PROJECT_FOLDER,
    PublishRabbitMessage,
    sellers_list_file_path,
    customers_list_file_path,
    global_config
)

from resource import (
    SellerRequestStatusIdentified,
    sync_db,
    LoggerSetup,
    CustomerOrderStatus,
    FilterCountries,
    TypeCar,
    ChatStatus,
    SellerOfferStatus,
    PhotoNaming,
    OrderMatchingStatus
)

logger_folder_api_mobile = PROJECT_FOLDER + "/project_logs"
if not os.path.exists(logger_folder_api_mobile):
    os.makedirs(logger_folder_api_mobile)

class BaseResponse(ABC):
    def init(self):
        pass

    @property
    @abstractmethod
    def error_500_response(self):
        pass

    @property
    @abstractmethod
    def error_406_response(self):
        pass

    @property
    @abstractmethod
    def error_401_response(self):
        pass

    @property
    @abstractmethod
    def user_not_found(self):
        pass

    @property
    @abstractmethod
    def deactivated_user_response(self):
        pass

    @property
    @abstractmethod
    def taken_email_response(self):
        pass

    @property
    @abstractmethod
    def taken_title_response(self):
        pass


class RuResponse(BaseResponse):
    @property
    def error_500_response(self):
        return "Ошибка сервера"

    @property
    def error_406_response(self):
        return "Ошибка аргументов"

    @property
    def error_401_response(self):
        return "Время сесси истекло"

    @property
    def user_not_found(self):
        return "Неверный логин/пароль"

    @property
    def deactivated_user_response(self):
        return "Аккаунт был деактивирован"

    @property
    def taken_email_response(self):
        return "Указанный email занят"

    @property
    def taken_title_response(self):
        return "Указанное название уже существует"


class Lang:
    def __init__(self):
        self.en = "en"
        self.ru = "ru"

        self.available_languages = [self.ru]

        self.default_language = self.ru


class Composer(Lang):
    """
        при наличии двух языков get и get_dict работают примерно одинакво
    """
    def __init__(self):
        super().__init__()
        self.ru_response = RuResponse()

        self.__switcher__ = {
            self.ru: self.ru_response
        }

        self.default_lang = self.ru_response

    def __call__(self, lang):
        return self.__switcher__.get(lang, self.default_lang)

    async def get(self, lang: Lang):
        if lang == self.ru:
            return self.ru_response
        else:
            return self.default_lang

    async def get_dict(self, lang: Lang):
        return self.__switcher__.get(lang, self.default_lang)


def init_error_logger():
    logger = logging.getLogger('error')
    logger.setLevel(logging.ERROR)

    log_formatter = logging.Formatter('%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s')
    my_handler = RotatingFileHandler(
        logger_folder_api_mobile + "/error.log",
        maxBytes=5 * 1024 * 1024,
        backupCount=10)
    my_handler.setFormatter(log_formatter)
    my_handler.setLevel(logging.ERROR)

    logger.addHandler(my_handler)

    return logger


def init_info_logger():
    logger = logging.getLogger('info')
    logger.setLevel(logging.INFO)

    log_formatter = logging.Formatter('%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s')
    my_handler = RotatingFileHandler(
        logger_folder_api_mobile + "/info.log",
        maxBytes=5 * 1024 * 1024,
        backupCount=10)
    my_handler.setFormatter(log_formatter)
    my_handler.setLevel(logging.INFO)

    logger.addHandler(my_handler)

    return logger

logger = LoggerSetup(path='./api_admin')
log_error = init_error_logger()
log_info = init_info_logger()

BASE_URL = '/api/v1/admin'
composer = Composer()
lang = Lang()

publish_rabbit_message = PublishRabbitMessage()
sellerRequestStatus = SellerRequestStatusIdentified()
customer_order_status = CustomerOrderStatus()
order_matching_status = OrderMatchingStatus()
chat_status = ChatStatus()
seller_offer_status = SellerOfferStatus()
filter_countries = FilterCountries()
type_car = TypeCar()

global_config = global_config
filter_countries = FilterCountries()

photo_naming = PhotoNaming()