#!/usr/bin/python

# Welcome to Doc Robot, aka Dokurobotto K-176 aka DR
# The do-some-things robot.

# This is the version number.
VERSION = "1"

# DR is brought to you in part by:
import ConfigParser
import imp, logging, os, re, signal, sys
from time import strftime

# And friends:
from ircutils import bot, ident, start_all


# Load up the commands. Let's find a better way to do this though, ok?
# Modules or something, I've heard of them. Look it up maybe?
from plugins.youtube.ident import YouTubeIdent

command_list = [YouTubeIdent]
regexes = [rx.regex for rx in command_list]

# Let's load stuff from the config file.
Config = ConfigParser.ConfigParser()
Config.read("settings.ini")

# -d = debug mode.
if "-d" in sys.argv or "--debug" in sys.argv:
    VERSION = "X"
    DEBUG = True
else:
    DEBUG = False


BASENAME = Config.get("Bot", "NAME")
NAME = "{0}-{1}".format(BASENAME, VERSION)

SERVER = Config.get("Network", "ADDRESS")

# Get the list of channels DR will join.
if DEBUG:
    CHANNELS = Config.get("Channels", "DEBUG")
else:
    CHANNELS = Config.get("Channels", "CHANS")

# Open the log.
logging.basicConfig(filename='robotlog.log', level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%m/%d %H:%M:%S')

# And now the star of our show!
class DocRobot(bot.SimpleBot):
    """DocRobot - the do-some-things IRC robot."""
    def talkback(self, event, actualtarget):
        for i, rx in enumerate(regexes):
            if re.search(rx, event.message):
                plugin_response = command_list[i](event)
                # Plugins can respond with either
                try:
                    self.send_message(actualtarget, plugin_response.pretty)
                except:
                    if DEBUG: logging.debug("{0} for <{1}> {2}".format(plugin_response.pretty, event.source, event.message))


    def on_join(self, event):
        """On any channel join"""
        pass

    def on_welcome(self, event):
        """After MOTD/welcome message event"""
        for chan in CHANNELS.split(","):
            logging.info("JOIN: {0}".format(chan))
            self.join(chan)

    def on_channel_message(self, event):
        """On any public message on any channel"""
        self.talkback(event, event.target)

    def on_private_message(self, event):
        """On any private message with DocRobot"""
        self.talkback(event, event.source)

    def goodbye(self, qmsg="ctrl-c"):
        """Ensures an actual disconnection if possible."""
        logging.info("good bye.")
        logging.info("----------------------------------------------------------------")
        docrobot.disconnect("ctrl-c")
        sys.exit(0)


# Log the quit and leave somewhat gracefully.
def signal_handler(signal, frame):
    """Capture ctrl-c terminations as noteable, but exit gracefuly."""
    logging.warning("Terminated by Console")
    docrobot.goodbye()

signal.signal(signal.SIGINT, signal_handler)

# Obligatory execution line
if __name__ == "__main__":
    logging.info("{0} connecting to {1}.".format(NAME, SERVER))
    docrobot = DocRobot(NAME)
    docrobot.connect(SERVER)

    # Setup the ident server, this reduces startup times by a lot.
    # TODO: This doesn't seem to be working, investigate.
    identd = ident.IdentServer(port=1113)

    start_all()
