from collections import OrderedDict
import json
import os
import random
import string
from unittest import TestCase

import mock

from .. import pop3

TEST_DATA_DIR = os.path.join(
    os.path.dirname(__file__),
    'test_data'
)


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

    # Each message is a tuple of (lines, msg_size). There are 4 messages.
    MESSAGES = OrderedDict(
        (message, data)
        for message, data in enumerate(
            json.loads(
                open(os.path.join(TEST_DATA_DIR, 'data.json'), 'r').read()
            ),
            start=1
        )
    )

    MAILBOX_SIZE = sum(msgsize for _, msgsize in MESSAGES.itervalues())

    instance = None

    def __init__(self, host, port):
        assert not self.connected
        self._connected = True
        self._host = host
        self._port = port
        self._user = None
        self._password = None
        MockPOP.instance = self

    def user(self, user):
        self._user = user
        return '+OK password required for user "%s"' % user

    def pass_(self, password):
        assert self._user is not None
        self._password = password
        return '+OK mailbox "%s" has %d messages (%d octets) H mockitymock' % (
            self._user, len(self.MESSAGES), self.MAILBOX_SIZE
        )

    def stat(self):
        return len(self.MESSAGES), self.MAILBOX_SIZE

    def retr(self, message):
        return ['+OK'] + self.MESSAGES[message]

    def quit(self):
        pass

def makeMockPOP(*args, **kwargs):
    return MockPOP(*args, **kwargs)

@mock.patch('poplib.POP3_SSL', new=makeMockPOP)
class TestPOP3(TestCase):

    # Provide long messages when asserts fail
    longMessage = True

    def test_login(self):
        host = os.environ['POP3_HOST'] = random_string()
        port = random.randint(1024, 65535)
        os.environ['POP3_PORT'] = str(port)
        user = os.environ['POP3_USER'] = random_string()
        password = os.environ['POP3_PASSWORD'] = random_string()

        messages = list(pop3.process_pop3_messages())

        # Verify that we logged in correctly
        self.assertEqual(MockPOP.instance._host, host)
        self.assertEqual(MockPOP.instance._port, port)
        self.assertEqual(MockPOP.instance._user, user)
        self.assertEqual(MockPOP.instance._password, password)

        self.assertEqual(
            len(messages),
            len(MockPOP.MESSAGES),
            'Verifying message count'
        )

