import pathlib
import json
import os


def dumpData(fqfn: str, data: dict | list) -> str:
    """
    dumps the data to the file name specified

    Args:
        fqfn (str): file name, including path
        data (_type_): data to be saved to file as JSON

    Returns:
        str: file name, including path
    """
    pathlib.Path(os.path.split(fqfn)[0]).mkdir(parents=True, exist_ok=True)
    with open(fqfn, "w") as wtr:
        json.dump(data, wtr, indent=4)
    return fqfn


def loadData(fqfn: str, defaultData: dict | list = None, saveDefaultIfNotExist: bool = False) -> dict | list:
    """
    loads JSON data from the file specified

    Args:
        fqfn (str): file name, including path
        defaultData (_type_, optional): default data if the file does not exist. Defaults to None

    Returns:
        dict | list: JSON data from the file
    """
    if not os.path.exists(fqfn):
        if saveDefaultIfNotExist:
            dumpData(fqfn, defaultData)
        return defaultData
    with open(fqfn) as rdr:
        return json.load(rdr)
