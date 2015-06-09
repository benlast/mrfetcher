import logging
import os
import poplib
from _socket import socket


OK = '+OK'


def get_pop3_messages():
    """
    Assuming that the environment defines:
     POP3_HOST
     POP3_PORT
     POP3_USER
     POP3_PASSWORD
    Connect to the host, retrieve a list of all the existing messages
    and yield each one as a tuple of (message-id, lines, msg_size)
    This is a coroutine generator - after each message has been
    yielded, the caller may pass True or False back into the flow to
    indicate that the message has been successfully forwarded and may
    be deleted (True) or that it could not be forwarded and should be
    left in the mailbox (False).
    """
    host = os.getenv('POP3_HOST', '')
    port = int(os.getenv('POP3_PORT', 110))
    try:
        pop = poplib.POP3_SSL(
            host,
            port
        )
    except socket.error as ex:
        logging.error(
            'Could not connect to "%s", port %d: %s',
            host, port, ex
        )
        return

    user = os.getenv('POP3_USER')
    password = os.getenv('POP3_PASSWORD')
    response = pop.user(user)
    if not response.startswith(OK):
        logging.error(
            'Could not log in as user "%s" (bad response from pop.user: "%s")',
            user, response
        )
    else:
        response = pop.pass_(password)
        if not response.startswith(OK):
            logging.error(
                'Could not log in as user "%s" '
                '(bad response from pop.pass: "%s")',
                user, response
            )
        else:
            messages, _ = pop.stat()
            for message in xrange(1, messages+1):
                try:
                    response, lines, msg_size = pop.retr(message)
                except poplib.error_proto as ex:
                    logging.warning(
                        'Could not retrieve message %d, error %s',
                        message, ex
                    )
                else:
                    if response.startswith(OK):
                        if (yield message, lines, msg_size):
                            pop.dele(message)
                    else:
                        logging.warning(
                            'Unexpected response retrieving message %d: %s',
                            message, response
                        )

            pop.quit()
