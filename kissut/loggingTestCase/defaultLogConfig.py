LOG_DEFAULT_CONFIG = {
    "version": 1,
    "formatters": {"default": {"format": "%(levelname)-8s | %(asctime)s | %(module)-30s | %(funcName)-30s | %(message)s"}},
    "handlers": {
        "console": {"class": "logging.StreamHandler", "stream": "ext://sys.stdout", "formatter": "default"},
        "file": {
            "class": "logging.FileHandler",
            "filename": "wkdir/unittest/log.txt",
            "formatter": "default",
            "encoding": "utf-8",
        },
    },
    "root": {"level": "DEBUG", "handlers": ["file"]},
}
