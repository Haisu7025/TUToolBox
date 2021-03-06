# -*- coding: utf-8 -*-

import configparser
import os


def getConfig(section="", key=""):
    config = configparser.ConfigParser()
    path = "../user.conf"
    config.read(path)
    print os.path.exists(path)
    return config.get(section, key)


def setConfig(section="", key="", value=""):
    config = configparser.ConfigParser()
    path = "../user.conf"
    config.read(path)
    config.add_section("user")
    config.set(section, key, value)
    config.write(open("user.conf", "w"))
