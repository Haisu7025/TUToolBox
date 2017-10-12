import configparser
import os


def getConfig(section="", key=""):
    config = configparser.ConfigParser()
    path = os.path.split(os.path.realpath(__file__))[0] + '/user.conf'
    print path


getConfig()
