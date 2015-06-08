from unittest import TestCase

import mock


class MockPOP(object):
    connected = False
    logged_in = False

    MESSAGES = [

    ]

    def __init__(self, host, port):
        assert not self.connected
        self.connected = True
        self.user = None
        self.password = None

    def user(self, user):
        self.user = user
        return '+OK password required for user "%s"' % user

    def pass_(self, password):
        assert self.user is not None
        return

class TestPOP3(TestCase):
    def test_login(self):
        pass
