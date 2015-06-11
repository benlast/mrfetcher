import logging
import poplib
import socket


OK = '+OK'


def process_pop3_messages(host, port, user, password, sender):
    """
    Connect to the host, retrieve a list of all the existing messages
    and send() each one as a tuple of (message-id, lines, msg_size)
    to the given sender (assumed to be a coroutine).
    This is a coroutine producer - after each message has been
    sent, the sender may yield True or False back into the flow to
    indicate that the message has been successfully forwarded and may
    be deleted (True) or that it could not be forwarded and should be
    left in the mailbox (False).
    """
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
            for message_id in xrange(1, messages+1):
                try:
                    response, lines, msg_size = pop.retr(message_id)
                except poplib.error_proto as ex:
                    logging.warning(
                        'Could not retrieve message %d, error %s',
                        message_id, ex
                    )
                else:
                    if response.startswith(OK):
                        logging.debug(
                            'POP3 message %d, size %d',
                            message_id, msg_size
                        )
                        if sender.send(message_id, lines, msg_size):
                            logging.debug('POP3 message %d to be deleted',message_id)
                            #pop.dele(message_id)
                    else:
                        logging.warning(
                            'Unexpected response retrieving message %d: %s',
                            message_id, response
                        )

            pop.quit()
            sender.close()

