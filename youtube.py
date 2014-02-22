#!/usr/bin/python

"""
This is DR's YouTube Module.
Features:
    - youTubeIdent():       Finds YT urls, and identifies them for the chat.
        - youTubeLogger():  Remember what URLs are sent from what channel.
    - youTubeSearch():      Uses YT's API to search for the top video given a query.
"""

import ConfigParser
import re
import logging
from urllib2 import urlopen, HTTPError
from BeautifulSoup import BeautifulSoup
from ircutils import format

# Some API stuff for youTubeSearch.
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# Let's load stuff from the config file.
Config = ConfigParser.ConfigParser()
Config.read("settings.ini")

APIKEY = Config.get("API", "YOUTUBEKEY")

# YouTube URL parser/identifier.
class YouTubeIdent:
    regex = re.compile("(?<=v(\=|\/))(?P<vid1>[-a-zA-Z0-9_]+)|(?<=youtu\.be\/)(?P<vid2>[-a-zA-Z0-9_]+)")
    desc = "Youtube Parsing: Automagically pulls video titles."

    def __init__(self, **kwargs):
        self.event = kwargs['event']
        
    def default_response(self):
        """ This will take a YouTube URL and output info about it.
        INPUT: http://youtu.be/WILNAdHli0k or http://www.youtube.com/watch?v=WILNAdHli0k
        OUTPUT: *** YouTube: Ultra and the Lazer Hearts - The Meth Minute 39 (93")
        """
        rx = re.compile(self.regex)
        rd = rx.search(self.event.message)
        rd = rd.groupdict()
        vidid = rd['vid1'] if rd['vid1'] else rd['vid2']

        # Use BeautifulSoup to parse the XML response.
        url = "http://gdata.youtube.com/feeds/api/videos/{0}".format(vidid)
        try:
            soup = BeautifulSoup(urlopen(url))
        except HTTPError:
            logging.warning("Bad video ID: {0} [{1}]".format(vidid, self.event.message))
            return ""
        vidsoup = soup.find(attrs={"medium": "video"})

        # Build the string.
        youtubeprefix = format.bold("*** YouTube: ")
        videotitle = format.underline(soup.title.string)
        videotitle = format.bold(videotitle)
        duration = format.filter(' ({0}")'.format(vidsoup['duration']))
        videoinfo = youtubeprefix + videotitle + duration

        # Log the YouTube videos DR identifies.
        self.videoLogger(vidid, self.event.target)

        return videoinfo.encode("utf-8")

    def videoLogger(self, vid, msgtarget):
        logging.debug("youTubeLogger() {0} from {1}".format(vid, msgtarget))
        pass
