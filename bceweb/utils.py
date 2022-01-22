import sys

from . import vars


# 5. utils
def eprint(s: str):
    """
    Print err/warning message to stderr
    :param s:
    :return: None
    """
    print(s, file=sys.stdout)


def vprint(s: str):
    """
    Print message in verbosity mode
    :param s: message
    :return: None
    """
    if vars.DEBUG:
        eprint(s)
