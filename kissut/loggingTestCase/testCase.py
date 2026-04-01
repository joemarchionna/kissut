from kissut.testData.files import loadData, dumpData
from kissut.loggingTestCase.logDirectory import initializeLogging
from kissut.testData.data import logConfigFile, loadConfigData
from kissut.testData.text import randStr
from types import FunctionType
from functools import wraps
import threading
import unittest
import logging

# ----
# loggingDecorator and MethodLoggingClass are used to wrap test methods and just add a logging line when entering


def loggingDecorator(testMethod):
    # logMethodAboutToRun is the wrapper function
    @wraps(testMethod)
    def logMethodAboutToRun(*args, **kwargs):
        lggr = logging.getLogger(__name__)
        # log the name of the test method about to be run
        lggr.debug("---- Running '{}' ----".format(testMethod.__name__))
        _result = testMethod(*args, **kwargs)
        # log that the test method has finished if desired
        return _result

    return logMethodAboutToRun


class MethodLoggingClass(type):
    def __new__(meta, classname, bases, classDict):
        newClassDict = {}
        for attributeName, attribute in classDict.items():
            if attributeName.startswith("test") and isinstance(attribute, FunctionType):
                # replace it with a wrapped version
                attribute = loggingDecorator(attribute)
            newClassDict[attributeName] = attribute
        return type.__new__(meta, classname, bases, newClassDict)


_THRD_LOCK = threading.Lock()


class LoggingTestCase(unittest.TestCase, metaclass=MethodLoggingClass):
    workingDirectory = None

    @classmethod
    def setUpClass(cls):
        if not LoggingTestCase.workingDirectory:
            with _THRD_LOCK:
                if not LoggingTestCase.workingDirectory:
                    LoggingTestCase.workingDirectory = initializeLogging(logConfigFilename=logConfigFile())
        cls.logger = logging.getLogger(__name__)
        cls.logger.debug("-- Entering {}".format(cls.__name__))

    @classmethod
    def tearDownClass(cls):
        # cls.logger.removeHandler(cls.handler)
        pass

    @classmethod
    def getConfig(cls) -> dict | list:
        """
        returns the configuration data from the working directory

        Returns:
            dict | list: configuration data from JSON
        """
        return loadConfigData()

    def loadWkDirData(self, filename: str = "data.json", defaultData: dict | list = None) -> dict | list:
        """
        prefixes the working directory to the filename provided, include subdirectories\n
        to the working directory if you like, ie: 'test_a/data.json

        Args:
            filename (str, optional): file name. Defaults to "data.json"
            defaultData (dict | list, optional): data to return if file does not exist. Defaults to None

        Returns:
            dict | list: data from JSON
        """
        fqfn = LoggingTestCase.workingDirectory + filename
        return loadData(fqfn, defaultData)

    def loadAnyData(self, fqfn: str, defaultData: dict | list = None) -> dict | list:
        """
        loads json data from anywhere, provide a fqfn

        Args:
            fqfn (str): file name and path
            defaultData (dict | list, optional): data to return if file does not exist. Defaults to None

        Returns:
            dict | list: data from JSON
        """
        return loadData(fqfn, defaultData)

    def dumpWkDirData(self, data: dict | list, filename="data.json") -> str:
        """
        prefixes the working directory to the filename provided, include subdirectories\n
        to the working directory if you like, ie: 'test_a/data.json

        Args:
            data (dict | list): data to save to JSON
            filename (str): file name

        Returns:
            str: file name and path
        """
        fqfn = LoggingTestCase.workingDirectory + filename
        return dumpData(fqfn, data)

    def dumpAnyData(self, data: dict | list, fqfn: str) -> str:
        """
        dumps data to JSON anywhere, provide a fully qualifed file name

        Args:
            data (dict | list): data to save to JSON
            fqfn (str): file name and path

        Returns:
            str: _description_
        """
        return dumpData(fqfn, data)

    def randString(self, size: int = 5):
        """
        returns a random string of length size

        Args:
            size (int, optional): length of the string returned. Defaults to 5

        Returns:
            str: random string
        """
        return randStr(size)
