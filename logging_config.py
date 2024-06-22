import logging
import logging.config
import os
from app.utils.log_filter import RelevantLogFilter

log_directory = 'logs'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
    },
    'filters': {
        'relevant': {
            '()': RelevantLogFilter,
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'filters': ['relevant'],
        },
        'file_macro': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'standard',
            'filename': os.path.join(log_directory, 'macro.log'),
            'filters': ['relevant'],
        },
        'file_csv': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'standard',
            'filename': os.path.join(log_directory, 'csv.log'),
            'filters': ['relevant'],
        },
        'file_consolidated': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'standard',
            'filename': os.path.join(log_directory, 'consolidated.log'),
            'filters': ['relevant'],
        },
    },
    'loggers': {
        'macro': {
            'handlers': ['file_macro', 'file_consolidated'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'csv': {
            'handlers': ['file_csv', 'file_consolidated'],
            'level': 'DEBUG',
            'propagate': False,
        },
        '': {
            'handlers': ['console', 'file_consolidated'],
            'level': 'DEBUG',
        },
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
