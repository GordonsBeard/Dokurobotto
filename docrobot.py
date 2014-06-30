#!/usr/bin/python
# -*- coding: utf-8 -*-

# Welcome to Doc Robot, aka Dokurobotto K-176 aka DR
# The do-some-things robot.

# This is the version number.

import config, imp, logging, os, re, signal, sys
from time import strftime

# And friends:
from ircutils import bot, ident, start_all

# DR's Modules are all in the plugins/ folder. This calls them all.
from plugins.youtube.ident import YouTubeIdent
from plugins.youtube.search import YouTubeSearch

# This will be active responses, !commands. Only one triggers.
# Looks for matching regex in Command.regex
active_command_list = [YouTubeSearch]
active_regexes = [rx.regex for rx in active_command_list] if active_command_list is not 0 else None

# These are the passive commands, each one gets a look at the string.
# Must have leinient regex to be picked up, or not. 
passive_command_list = [YouTubeIdent]
passive_regexes = [rx.regex for rx in passive_command_list] if passive_command_list is not 0 else None

# Open the log.
logging.basicConfig(filename='robotlog.log', level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%m/%d %H:%M:%S')

# And now the star of our show!
class DocRobot(bot.SimpleBot):
    """DocRobot - the do-some-things IRC robot."""

    def active_talkback(self, event, actualtarget):
        """ One command, one message. """
        if active_regexes is None: return
        for i, rx in enumerate(active_regexes):
            if re.search(rx, event.message):
                # Cycle through the active commands first.
                # TODO set up order of operations for active commands?
                plugin_responses = active_command_list[i](event)
                if plugin_responses.pretty is not None:
                    try:
                        """ We call the plugin if the response matches.
                        The plugin itself returns a list of responses in .pretty
                        ex: YouTubeSearch.pretty = ['youtu.be/video', 'title: video thing (post 3)']
                        """
                        for message in plugin_responses.pretty:
                            self.send_message(actualtarget, message)
                    except Exception, e:
                        # If this has some error and we're in debug, log it.
                        # Otherwise fail silently? Hm.
                        print "NOPE"
                        print e
                        for message in plugin_responses.pretty:
                            if config.DEBUG: logging.debug("** ERROR:\t{0} for <{1}> {2}".format(plugin_responses.pretty, event.source, event.message))
                    return

    def passive_talkback(self, event, actualtarget):
        """ Multiple passive commands, one message. """
        for i, rx in enumerate(passive_regexes):
            if re.search(rx, event.message):
                plugin_responses = passive_command_list[i](event)
                if plugin_responses.pretty is not None:
                    try:
                        for message in plugin_responses.pretty:
                            self.send_message(actualtarget, message)
                    except:
                        # If this has some error and we're in debug, log it.
                        # Otherwise fail silently? Hm.
                        for message in plugin_responses.pretty:
                            if config.DEBUG: logging.debug("** ERROR:\t{0} for <{1}> {2}".format(message, event.source, event.message))
            

    def on_join(self, event):
        """ Executes on any channel join. """
        pass

    def on_welcome(self, event):
        """ After MOTD/welcome message event """

        # Join the channels.
        for chan in config.CHANNELS.split(","):
            logging.info("JOIN: {0}".format(chan))
            self.join(chan)

    def on_channel_message(self, event):
        """ On any public message on any channel """
        self.active_talkback(event, event.target)
        self.passive_talkback(event, event.target)

    def on_private_message(self, event):
        """ On any private message with DocRobot """
        self.active_talkback(event, event.source)
        self.passive_talkback(event, event.source)

    def goodbye(self, qmsg="ctrl-c"):
        """ Ensures an actual disconnection if possible."""
        logging.info(config.QUIT)
        logging.info("----------------------------------------------------------------")
        docrobot.disconnect(config.QUIT)
        sys.exit(0)


# Log the quit and leave somewhat gracefully.
def signal_handler(signal, frame):
    """ Capture ctrl-c terminations as noteable, but exit gracefuly. """
    logging.warning("Terminated by Console")
    docrobot.goodbye()

signal.signal(signal.SIGINT, signal_handler)

# Obligatory execution line
if __name__ == "__main__":
    """ ./docrobot.py [-d] """
    name = config.NAME
    server = config.SERVER

    logging.info("{0} connecting to {1}.".format(name, server))
    docrobot = DocRobot(name)
    docrobot.connect(server)

    # Setup the ident server, this reduces startup times by a lot.
    # TODO: This doesn't seem to be working, investigate.
    identd = ident.IdentServer(port=1113)

    start_all()
