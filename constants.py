import logging

class Constants:
    APP_CONFIG_FILE_PATH = 'tapad_analytics_task.json'
    DEFAULT_REDIS_MAX_CONN = 20
    DEFAULT_REDIS_HOST = 'redis'
    DEFAULT_REDIS_PORT = 6379
    DEFAULT_REDIS_DATABASE = 0
    DEFAULT_REDIS_PASSWORD = 'ORQXAYLE'
    LOG_LEVEL = 'DEBUG'
    LOGGING_LEVELS = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }
    LOG_FILE = 'tapad_analytics_task.log'
    APP_HOST = '0.0.0.0'
    APP_PORT = 5000
    ISO_TIME_FORMAT = '%Y-%m-%d %H:%M:%S.%f'
