#!/usr/bin/python
"""
This is DR's YouTube Module.
Features:
    - youTubeIdent():       Finds YT urls, and identifies them for the chat.
        - youTubeLogger():  Remember what URLs are sent from what channel.
    - youTubeSearch():      Uses YT's API to search for the top video given a query.
"""

import re
from urllib2 import urlopen, HTTPError
from BeautifulSoup import BeautifulSoup
from ircutils import format


# YouTube URL parser/identifier.
class YouTubeIdent:
    """Class for containg the YouTube message and it's chat-friendly translation.
    Returns obj.message: the triggering message
            obj.source: the source of the triggering message
            obj.target: the target of the triggering message
            obj.pretty: the pretty string that's sent to chat
            obj.vidid: the video id"""

    regex = re.compile("(?<=v(\=|\/))(?P<vid1>[-a-zA-Z0-9_]+)|(?<=youtu\.be\/)(?P<vid2>[-a-zA-Z0-9_]+)")

    def __init__(self, event, log=True):
        self.message = event.message
        self.source = event.source
        self.target = event.target

        rx = re.compile(self.regex)
        rd = rx.search(self.message)
        rd = rd.groupdict()
        self.vidid = rd['vid1'] if rd['vid1'] else rd['vid2']

        self.pretty = self.get_videoinfo()

        self.log = self.logVideo(event) if log else None

    def get_videoinfo(self):
        # Use BeautifulSoup to parse the XML response.
        url = "http://gdata.youtube.com/feeds/api/videos/{0}".format(self.vidid)
        try:
            soup = BeautifulSoup(urlopen(url))
        except HTTPError, e:
            return e 

        vidsoup = soup.find(attrs={"medium": "video"})

        # Build the string.
        youtubeprefix = format.bold("*** YouTube: ")
        videotitle = format.underline(soup.title.string)
        videotitle = format.bold(videotitle)
        duration = format.filter(' ({0}")'.format(vidsoup['duration']))
        videoinfo = youtubeprefix + videotitle + duration

        return videoinfo.encode("utf-8")

    def logVideo(self, event):
        pass
