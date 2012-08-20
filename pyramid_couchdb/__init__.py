# Copyright (c) 2011-2012 Ryan Bourgeois <bluedragonx@gmail.com>
#
# This project is free software according to the BSD-modified license. Refer to
# the LICENSE file for complete details.
"""
Package implementing CouchDB support in Pyramid.
"""

from couchdbkit import Server
from pyramid.events import NewRequest


__all__ = ['Session', 'session', 'configure']

class Session:

    """
    Store session information.
    """

    uri_key = 'couchdb.uri'

    def __init__(self):
        """
        Initialize the object. Sets the value of self.uri_key to
        'couchdb.uri'.
        """
        self.configured = False
        self.uri = None
        self._server = None

    def configure(self, settings):
        """
        Configure the session. Attempts to look up the uri using the value of
        self.uri_key as the settings key.
        """
        if self.uri_key in settings:
            self.uri = settings[self.uri_key]
        else:
            self.uri = None
        self._server = None
        self.configured = True

    @property
    def server(self):
        """The server object."""
        if self._server is None:
            if self.uri is None:
                self._server = Server()
            else:
                self._server = Server(self.uri)
        return self._server


session = Session()


def request_event_handler(event):
    """
    Add the session server object to a request.
    
    The server is set on the request's couch attribute. So, for example, to
    access a database named auth:
      request.couch['auth']
    """
    if not session.configured:
        session.configure(event.request.registry.settings)
    event.request.couch = session.server


def configure(config):
    """Configure Pyramid to use CouchDB."""
    settings = config.get_settings()
    if not session.configured:
        session.configure(settings)
    config.add_subscriber(request_event_handler, NewRequest)
    return config

