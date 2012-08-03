# Copyright (c) 2011-2012 Ryan Bourgeois <bluedragonx@gmail.com>
#
# This project is free software according to the BSD-modified license. Refer to
# the LICENSE file for complete details.
"""
Test pyramid_couchdb module functionality.
"""

import unittest
import pyramid_couchdb
from pyramid.testing import DummyRequest
from couchdbkit import Server


class DummyConfig:

    """
    Dummy Pyramid config class.
    """

    def __init__(self):
        """Initialize dummy config data."""
        self.settings = {'couchdb.uri': 'http://localhost:5984/'}
        self.subscribers = []

    def get_settings(self):
        """Get the settings object."""
        return self.settings

    def add_subscriber(self, handler, eventtype):
        """Add an event subscriber to the dummy."""
        self.subscribers.append((handler, eventtype))

    def has_subscriber(handler, eventtype):
        """Check if a subscriber has been added to handle an event type."""
        subs = [sub for sub in self.subscribers
            if sub[0] == handler and sub[1] == eventtype]
        return subs.len() > 0


class DummyRegistry:

    """
    Dummy Pyramid registry class.
    """

    def __init__(self, settings=None):
        """Initialize dummy data."""
        self.settings = settings


class DummyEvent:

    """
    Dummy Pyramid event class.
    """

    def __init__(self, config):
        """Initialize dummy event data."""
        self.request = DummyRequest()
        self.request.registry = DummyRegistry(config.get_settings())


class TestSession(unittest.TestCase):

    """
    Test the Session class.
    """

    def setUp(self):
        """Initialize test data."""
        pyramid_couchdb.session = pyramid_couchdb.Session()
        self.settings = {
            'couchdb.uri': 'http://localhost:5984/',
            'couch.uri': 'http://127.0.0.1:5984/'}

    def test_init(self):
        """Test the __init__ method."""
        self.assertEqual(pyramid_couchdb.session.uri_key, 'couchdb.uri',
            'uri_key not set to default')
        self.assertTrue(pyramid_couchdb.session.uri is None,
            'uri not set to default')
        self.assertFalse(pyramid_couchdb.session.configured,
            'configured set to True')
        self.assertTrue(pyramid_couchdb.session._server is None,
            'server not set to default')

    def test_configure_default(self):
        """Test configure method with default uri_key value."""
        pyramid_couchdb.session.configure(self.settings)
        self.assertEqual(pyramid_couchdb.session.uri,
            self.settings['couchdb.uri'], 'uri not properly set')
        self.assertTrue(pyramid_couchdb.session.configured,
            'configured set to False')

    def test_configure_custom(self):
        """Test configure method with custom uri_key value."""
        pyramid_couchdb.session.uri_key = 'couch.uri'
        pyramid_couchdb.session.configure(self.settings)
        self.assertEqual(pyramid_couchdb.session.uri,
            self.settings['couch.uri'], 'uri not properly set')
        self.assertTrue(pyramid_couchdb.session.configured,
            'configured set to False')

    def test_server(self):
        """Test server property."""
        pyramid_couchdb.session.uri_key = 'couchdb.uri'
        pyramid_couchdb.session.configure(self.settings)
        server = pyramid_couchdb.session.server
        self.assertIsInstance(server, Server)


class TestModuleFunctions(unittest.TestCase):

    """
    Test the module functions.
    """

    def setUp(self):
        """Initialize test data."""
        pyramid_couchdb.session = pyramid_couchdb.Session()

    def test_request_event_handler(self):
        """Test the request_event_handler function."""
        config = DummyConfig()
        event = DummyEvent(config)
        pyramid_couchdb.request_event_handler(event)
        self.assertEqual(pyramid_couchdb.session.server, event.request.couch,
            'event request server does not match session server')

    def test_configure(self):
        """Test the configure function."""
        config = DummyConfig()
        pyramid_couchdb.configure(config)
        self.assertEqual(pyramid_couchdb.session.uri,
            config.settings['couchdb.uri'], 'failed to configure session')

