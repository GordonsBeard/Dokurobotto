#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Configuration stuff for the YouTube module.
"""
import sys

# Database names, edit these if you want.
default_name = 'videos.db'
debug_name = 'debug.db'

# Nothing below here to edit.

# -d, --debug: Debug mode, will enable more logging/verbosity.
if "-d" in sys.argv or "--debug" in sys.argv:
    DEBUG = True
else:
    DEBUG = False

# Set database constant.
DB_FILENAME = debug_name if DEBUG else default_name
