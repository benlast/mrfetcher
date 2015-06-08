import random
import string
from unittest import TestCase

import mock


def random_string(
        choose_from=None,
        length=8
):
    """
    Return a random sequence of characters
    :param choose_from: the set of eligible characters - by default
    the set is string.ascii_lowercase + string.digits
    :param length: the length of the sequence to be
    returned
    :return: the sequence
    """
    choices = choose_from or (string.ascii_lowercase + string.digits)
    return ''.join(
        random.choice(choices)
        for _ in xrange(length)
    )

class MockPOP(object):
    connected = False
    logged_in = False

    # Each message is a tuple of (headers, body)
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
