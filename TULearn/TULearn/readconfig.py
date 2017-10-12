# -*- coding: utf-8 -*-

import configparser
import os


def getConfig(section="", key=""):
    config = configparser.ConfigParser()
    path = os.path.split(os.path.realpath(__file__))[0] + '/user.conf'
    config.read(path)
    print os.path.exists(path)
    return config.get(section, key)


def setConfig(section="", key="", value=""):
    config = configparser.ConfigParser()
    path = os.path.split(os.path.realpath(__file__))[0] + '/user.conf'
    config.read(path)
    config.add_section("user")
    config.set(section, key, value)
    config.write(open("user.conf", "w"))


setConfig("user", "name", "test")
print getConfig("user", "name")
