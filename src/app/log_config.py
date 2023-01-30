from app.settings import get_settings

settings = get_settings()

log_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'},
        'simple': {
            'format': '%(asctime)s [%(levelname)s] %(name)s:%(filename)s:%(funcName)s:%(lineno)d - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'extended': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(funcName)s - %(message)s %(request)s %(response)s'
        },
        'sqlalchemy_format': {
            # TODO: bind params and pretty print
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'format': (
                "%(asctime)s [%(levelname)s] %(name)s:Start\n\n"
                "%(message)s\n\n"
                "%(asctime)s [%(levelname)s] %(name)s:End"
            ),
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'sqlalchemy_log': {
            'class': 'logging.StreamHandler',
            'formatter': 'sqlalchemy_format',
        },
        'uvicorn.error': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'uvicorn.access': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': settings.LOG_LEVEL,
        },
        'uvicorn.access': {
            'handlers': ['uvicorn.access'],
            'level': settings.LOG_LEVEL,
            "propagate": False,
        },
        'uvicorn.error': {
            'handlers': ['uvicorn.error'],
            'level': settings.LOG_LEVEL,
            "propagate": False,
        },
        "sqlalchemy.engine.Engine": {
            "handlers": ["sqlalchemy_log"],
            "level": settings.LOG_LEVEL,
            "propagate": False,
        },
    },
}
