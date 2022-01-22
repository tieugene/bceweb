import sys
from flask import current_app


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
    if current_app.config['DEBUG']:
        eprint(s)
