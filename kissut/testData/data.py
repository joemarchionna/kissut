from kissut.testData.files import dumpData, loadData
import logging
import os


def _getPaths() -> dict:
    d = {"logCfgFile": "wkdir/unittest/logConfig.json", "testCfgFile": "wkdir/unittest/testConfig.json"}
    altPath = os.getenv("UNITTEST_UTILS_CFG_FILE")
    if altPath:
        altData = loadData(altPath, d)
        d.update(altData)
    return d


TEST_PATHS = _getPaths()


def logConfigFile() -> str:
    """
    returns the log configuration file path

    Returns:
        str: file path
    """
    return TEST_PATHS["logCfgFile"]


def loadConfigData(fqfn: str = TEST_PATHS["testCfgFile"], defaultData=None, logName: str = None) -> dict:
    """
    loads a unittest JSON config file from a standard location

    Args:
        fqfn (str, optional): file name of the configuration data
        defaultData (_type_, optional): the default data to save to disk if the file doesn't exist. Defaults to None
        logName (str, optional): the log name to use. Defaults to None

    Returns:
        dict: configuration data
    """
    if not os.path.exists(fqfn) and not defaultData:
        dumpData(fqfn, {"key": "value", "dbConn": "host=hostdb dbname=dev user=devusr password=doh!", "data": {}})
        logging.getLogger(logName).critical("Config File '{}' Didn't Exist, Edit Appropriately And Run Tests Again".format(fqfn))
        exit()
    return loadData(fqfn, defaultData)
