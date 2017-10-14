import os
import sys
import getopt
import configparser

opts, args = getopt.getopt(sys.argv[1:], "u:p:")

username = ""
password = ""

for op, value in opts:
    if op == "-u":
        # account
        username = value
    elif op == "-p":
        # password
        password = value

config = configparser.ConfigParser()
config.read("user.conf")

config.add_section("user")
config.set("user", "username", username)
config.set("user", "userpass", password)

config.add_section("func")
config.set("func", "mail", "0")
config.write(open("user.conf", "w"))
