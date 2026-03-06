from kissut.loggingTestCase.defaultLogConfig import LOG_DEFAULT_CONFIG
from kissut.testData.files import loadData
from logging.config import dictConfig
import datetime
import pathlib
import os


def createUnittestWorkDir(directory: str) -> str:
    """creates the unittest working directory and subDirectory"""
    fullDir = "{}{}/".format(directory, datetime.datetime.now().strftime("%Y%m%dT%H%M%S"))
    pathlib.Path(fullDir).mkdir(parents=True, exist_ok=False)
    return fullDir


def _modifyRotatingFileName(filename: str, cfg: dict):
    if "handlers" in cfg:
        if "file" in cfg["handlers"]:
            if cfg["handlers"]["file"]["class"] == "logging.FileHandler":
                cfg["handlers"]["file"]["filename"] = filename


def initializeLogging(logConfigFilename: str) -> str:
    """returns the time-stamped unittest working directory"""
    wkDir = os.path.split(logConfigFilename)[0] + "/"
    wkDir = createUnittestWorkDir(wkDir)
    cfg = loadData(logConfigFilename, defaultData=dict(LOG_DEFAULT_CONFIG))
    _modifyRotatingFileName(wkDir + "log.txt", cfg)
    dictConfig(cfg)
    return wkDir
