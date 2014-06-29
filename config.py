#!/usr/bin/python
# -*- coding: utf-8 -*-
VERSION = "1"

import ConfigParser, sys

# -d = debug mode.
if "-d" in sys.argv or "--debug" in sys.argv:
    VERSION = "X"
    DEBUG = True
else:
    DEBUG = False

# Let's load stuff from the config file.
Config = ConfigParser.ConfigParser()
Config.read("settings.ini")


BASENAME = Config.get("Bot", "NAME")
NAME = "{0}-{1}".format(BASENAME, VERSION)

SERVER = Config.get("Network", "ADDRESS")

# Get the list of channels DR will join.
CHANNELS = Config.get("Channels", "DEBUG") if DEBUG else Config.get("Channels", "CHANS")

QUIT = Config.get("Bot", "QUIT")
