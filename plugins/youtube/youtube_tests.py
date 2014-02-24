#!/usr/bin/python
"""This tests the YouTube"""

import unittest
import ident
from ircutils.events import MessageEvent
from urllib2 import HTTPError

class TestYouTubeIdent(unittest.TestCase):
    """This is for testing the core identify function in the YouTube module."""

    user = "TestUser!testuser@test.com"
    channel = "#channel"

    prvmsg = "PRIVMSG"
    notice = "NOTICE"

    valid_url = "http://www.youtube.com/watch?v=iVAWm8VNmQA"
    valid_message = "have you guys seen http://youtu.be/iVAWm8VNmQA?"
    valid_response = '\x02*** YouTube: \x02\x02\x1fA Tribute to the Snackish\x1f\x02 (32")'

    invalid_url = "http://youtu.be/i333AWm8VNmQA"
    invalid_message = "they named their pokemon some garbage like ch?v=iVAW"
    error_400 = "HTTP Error 400: Bad Request"

    deleted_url = "http://www.youtube.com/watch?v=k-rjwg_9mdw"
    private_url = "http://youtu.be/IC0C5w1-T1Y"

    def test_valid_url(self):
        """This URL should pass with a valid response."""
        valid_message_event = MessageEvent(self.user, "PRIVMSG", [self.channel, self.valid_url])
        ytident = ident.YouTubeIdent(valid_message_event)
        self.assertEqual(ytident.pretty, self.valid_response)

    def test_valid_message(self):
        """This message should pass with a valid response."""
        valid_message_event = MessageEvent(self.user, "PRIVMSG", [self.channel, self.valid_message])
        ytident = ident.YouTubeIdent(valid_message_event)
        self.assertEqual(ytident.pretty, self.valid_response)

    def test_invalid_url(self):
        """Because this is an invalid URL, this should return an HTTPError exception"""
        valid_message_event = MessageEvent(self.user, "PRIVMSG", [self.channel, self.invalid_url])
        ytident = ident.YouTubeIdent(valid_message_event)
        self.assertEqual(type(ytident.pretty), HTTPError)

    def test_invalid_message(self):
        """Because this is an invalid message, this should return an HTTPError exception"""
        valid_message_event = MessageEvent(self.user, "PRIVMSG", [self.channel, self.invalid_message])
        ytident = ident.YouTubeIdent(valid_message_event)
        self.assertEqual(type(ytident.pretty), HTTPError)

    def test_deleted_video_url(self):
        """Because this is a deleted video, this should return an HTTPError exception"""
        valid_message_event = MessageEvent(self.user, "PRIVMSG", [self.channel, self.deleted_url])
        ytident = ident.YouTubeIdent(valid_message_event)
        self.assertEqual(type(ytident.pretty), HTTPError)

    def test_private_video_url(self):
        """Because this is a private video, this should return an HTTPError exception"""
        valid_message_event = MessageEvent(self.user, "PRIVMSG", [self.channel, self.private_url])
        ytident = ident.YouTubeIdent(valid_message_event)
        self.assertEqual(type(ytident.pretty), HTTPError)

def main():
    unittest.main()

if __name__ == "__main__":
    main()
