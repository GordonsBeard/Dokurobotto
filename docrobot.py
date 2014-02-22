#!/usr/bin/python

# Welcome to Doc Robot, aka Dokurobotto K-176 aka DR
# The do-some-things robot.

# This is the version number.
VERSION = "1"

# DR is brought to you in part by:
import ConfigParser
import logging, re, signal, sys
from ircutils import bot, ident, start_all
from time import strftime

# If -d was passed in we are in debug mode.
global DEBUG
try:
    if sys.argv[1] == "-d":
        VERSION = "X"
        DEBUG = True
except IndexError:
    DEBUG = False

# Let's load stuff from the config file.
Config = ConfigParser.ConfigParser()
Config.read("settings.ini")

BASENAME = Config.get("Bot", "NAME")
NAME = "{0}-{1}".format(BASENAME, VERSION)

SERVER = Config.get("Network", "ADDRESS")

# Get the list of channels we'll be joining.
if DEBUG:
    CHANNELS = Config.get("Channels", "DEBUG")
else:
    CHANNELS = Config.get("Channels", "CHANS")

GOOGLEAPI = Config.get("API", "YOUTUBEKEY")

# Open the log.
logging.basicConfig(filename='robotlog.log', level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%m/%d %H:%M:%S')

# What does DR respond to?
commandlist = []

class DRComm:
    def __init__(self, func, regex, desc, command=None):
        self.regex =  re.compile(regex)
        self.func = func
        self.desc = desc
        self.command = command
        commandlist.append(self)

    def __repr__(self):
        return "<Command('{0}', '{1}', '{2}', '{3}')>".format(self.func, self.regex, self.desc, self.command)

#   TODO Load these in a more modular way.
from youtube import YouTubeIdent
YouTubeCom = DRComm(YouTubeIdent, YouTubeIdent.regex, YouTubeIdent.desc)


# And now the star of our show, DR!
class DocRobot(bot.SimpleBot):
    def on_welcome(self, event):
        for chan in CHANNELS.split(","):
            logging.info("JOIN: #{0}".format(chan))
            self.join("#"+chan)

    def global_response(event):
        print event.items()

    def on_private_message(self, event):
        print event.items()

    def on_channel_message(self, event):
        for command in commandlist:
            if re.search(command.regex, event.message.lower()):
                retmessage = command.func(event = event)
                if DEBUG: logging.debug("s:{0} t:{1} m:{2}".format(event.source, event.target, retmessage))
                self.send_message(event.target, retmessage.default_response())

    def on_private_message(self, event):
        logging.info("PM: {0}\t{1}".format(event.source, event.message))
        for command in commandlist:
            if re.search(command.regex, event.message.lower()):
                retmessage = command.func(event = event)
                if DEBUG: logging.debug("s:{0} t:{1} m:{2}".format(event.source, event.target, retmessage))
                self.send_message(event.source, retmessage.default_response())

# Log the quit and leave somewhat gracefully.
def signal_handler(signal, frame):
    logging.warning("Terminated by Console")
    logging.info("-----------------------------------------------------------------------")
    docrobot.disconnect("ctrl-c")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Obligatory execution line
if __name__ == "__main__":
    logging.info("{0} connecting to {1}.".format(NAME, SERVER))
    docrobot = DocRobot(NAME)
    docrobot.connect(SERVER)

    # Setup the ident server, this reduces startup times by a lot.
    identd = ident.IdentServer(port=1113)

    start_all()
