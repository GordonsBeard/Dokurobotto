#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This is the YouTube identify module.
Features:
    - YouTubeIdent
        * log = True, set to False for PMs?
        - get_videoinfo():  Does the string building of the pretty output.
        - log_video():      Logs +1 view for the video in a sqlite3 db.
"""

import config, datetime, os, re, sqlite3
from urllib2 import urlopen, HTTPError
from BeautifulSoup import BeautifulSoup
from ircutils import format

# Check for database.
db_is_new = not os.path.exists(config.DB_FILENAME)

conn = sqlite3.connect(config.DB_FILENAME)
if config.DEBUG: print "Debug Mode, using database: {0}".format(config.DB_FILENAME)
if db_is_new:

    if config.DEBUG: print "Need to create schema."

    cursor = conn.cursor()
    cursor.execute('''
    create table videos (
        id integer primary key autoincrement,
        vidid string unique not null,
        posts integer not null,
        firstdate datetime not null,
        firstsource string not null,
        firsttarget string not null,
        lastdate datetime not null,
        lastsource string not null,
        lasttarget string not null
    )''')

    try:
        conn.commit()
        if config.DEBUG: print "Empty database created."
    except sqlite3.Error:
        if config.DEBUG: print "Error creating database."

conn.close()

print "YouTube module loaded."

# YouTube URL parser/identifier.
class YouTubeIdent:
    """ Class for containg the YouTube message and it's chat-friendly translation. """

    # Magic regex to pull out youtu.be/<vidid> or youtube.com/v?=<vidid>
    regex = re.compile("(?<=v(\=|\/))(?P<vid1>[-a-zA-Z0-9_]+)|(?<=youtu\.be\/)(?P<vid2>[-a-zA-Z0-9_]+)")


    def __init__(self, event):
        self.message = event.message
        self.source = event.source
        self.target = event.target

        rx = re.compile(self.regex)
        rd = rx.search(self.message)
        rd = rd.groupdict()
        self.vidid = rd['vid1'] if rd['vid1'] else rd['vid2']

        self.log = True if event.target[0] == "#" else False

        self.pretty = [self.get_videoinfo(),]


    def get_videoinfo(self):
        """ Returns a pretty string that in turn is used in YouTubeIdent.pretty """

        # Use BeautifulSoup to parse the XML response.
        url = "http://gdata.youtube.com/feeds/api/videos/{0}".format(self.vidid)
        try:
            soup = BeautifulSoup(urlopen(url))
        except HTTPError, e:
            return e

        vidsoup = soup.find(attrs={"medium": "video"})

        # If it doesn't exist, abort.
        if not vidsoup: return None

        # Build the string.
        youtubeprefix = format.bold("*** YouTube: ")
        videotitle = format.underline(soup.title.string)
        videotitle = format.bold(videotitle)
        duration = format.filter(' ({0}")'.format(vidsoup['duration']))
        reposts = self.get_view_count(self.log)
        repoststring = format.filter(' (post {0})'.format(reposts)) if reposts > 1 else ''
        videoinfo = youtubeprefix + videotitle + duration + repoststring

        return videoinfo.encode('utf-8')

    def get_view_count(self, log):
        """ Take the video, give it +1 posts or stuff it into the database forever.
            Returns the number of posts the video has. """
        conn = sqlite3.connect(config.DB_FILENAME)
        cursor = conn.cursor()

        cursor.execute("SELECT posts from videos WHERE vidid = ?", (self.vidid,))
        data = cursor.fetchone()

        if data and log is False:
            return data[0]

        elif data is not None:
            posts = data[0] + 1
            cursor.execute("UPDATE videos SET posts = posts + 1 WHERE vidid = ?", (self.vidid,))

        else:
            posts = 1
            cursor.execute("INSERT INTO videos (vidid, posts, firstdate, firstsource, firsttarget, lastdate, lastsource, lasttarget) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (self.vidid, 1, datetime.datetime.now(), self.source, self.target, datetime.datetime.now(), self.source, self.target))

        conn.commit()
        conn.close()
        return posts
