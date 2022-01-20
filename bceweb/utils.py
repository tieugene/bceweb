import configparser
import os
import sys

import vars


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


def init_cfg():
    """
    Init app variables
    :return:
    """
    cfg_real_path = os.path.expanduser(vars.CFG_FILE_NAME)
    if not os.path.exists(cfg_real_path):
        return
    config = configparser.ConfigParser()
    # config.read(cfg_real_path)
    config.read_string("[{}]\n{}".format(vars.CFG_MAIN_SECT, open(cfg_real_path, "rt").read()))
    config_default = config[vars.CFG_MAIN_SECT]
    # fill out
    vars.SECRET_KEY = config_default.get('secret', vars.SECRET_KEY)
    vars.DB_HOST = config_default.get('dbhost', vars.DB_HOST)
    vars.DB_NAME = config_default.get('dbname', vars.DB_NAME)
    vars.DB_USER = config_default.get('dbuser', vars.DB_USER)
    vars.DB_PASS = config_default.get('dbpass', vars.DB_PASS)
