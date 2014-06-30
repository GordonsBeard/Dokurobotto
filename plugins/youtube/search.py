#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This lets DR search YouTube by keyword.
    - YouTubeSearch

A ton of this was stolen from the Google examples for YouTube search.
https://github.com/youtube/api-samples/blob/master/python/search.py
"""

import config, re
from ident import YouTubeIdent
from ircutils.events import MessageEvent

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = config.YOUTUBEKEY
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

class YouTubeSearch:
    """ Class for containing the YouTube search result. """

    # Magic regex to get the query out of the !yt <query> message.
    regex = re.compile("((!yt) (?P<query>\".*\"|\w+))")

    def __init__(self, event):
        self.message = event.message
        self.source = event.source
        self.target = event.target

        rx = re.compile(self.regex)
        rd = rx.search(self.message)
        rd = rd.groupdict()
        self.query = rd['query']

        try:
            self.pretty = self.youtube_search(event, self.query) 
        except HttpError, e:
            print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
            self.pretty = None

    def youtube_search(self, event, query):
        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
            developerKey=DEVELOPER_KEY)

        # Call the search.list method to retrieve results matching the specified
        # query term.
        search_response = youtube.search().list(
            q=query,
            part="id,snippet",
            maxResults=5
        ).execute()

        videos = []

        # Add each result to the appropriate list, and then display the lists of
        # matching videos, channels, and playlists.
        for search_result in search_response.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":
                vidid = search_result['id']['videoId']
                if event.target[0] != "#":
                    target = event.source
                else:
                    target = event.target
                fake_message = "http://youtu.be/{0}".format(vidid)
                
                fake_event = MessageEvent(event.user, "PRVMSG", [target, fake_message])
                pretty_ident = YouTubeIdent(fake_event)

                return [fake_message, pretty_ident.pretty[0]] 
