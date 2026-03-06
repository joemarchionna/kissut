import os


def randStr(size=5) -> str:
    """
    returns a random string of length size

    Args:
        size (int, optional): length of the string returned. Defaults to 5

    Returns:
        str: random string
    """
    return str(os.urandom(size).hex())[:size]
