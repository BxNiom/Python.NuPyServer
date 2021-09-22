__version__ = '0.1.0'

import logging.config

LOG_CONFIG = {
    'disable_existing_loggers': False,
    'version': 1,
    'formatters': {
        'short': {
            'format': '%(asctime)s [%(levelname)-5s]: %(message)s'
        },
        'long': {
            'format': '%(asctime)s [%(levelname)-5s] [%(process)d] %(name)s - %(module)s: %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'formatter': 'short',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'INFO',
            'formatter': 'long',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/nupyserver.log',
            'maxBytes': 20000,
            'backupCount': 5
        }
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
        }
    },
}

logging.config.dictConfig(LOG_CONFIG)
