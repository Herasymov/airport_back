import os
from logging.handlers import RotatingFileHandler
import logging
from abc import abstractmethod, ABC


from resource import (
    sync_db,
    LoggerSetup,
    GlobalConfig,
    ConvertDateFormat
)

BASE_URL = '/api/v1'
logger = LoggerSetup(path='./api_admin')

global_config = GlobalConfig()
convert_date_format = ConvertDateFormat()
