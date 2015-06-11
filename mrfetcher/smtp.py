import collections
import logging
import itertools
import os
import re
import smtplib

from werkzeug.datastructures import MultiDict

HEADER_RE = re.compile(r'^[A-Za-z][-\w]*:\s*(.*)$', re.IGNORECASE)

def send_smtp_messages(
    smtp_host,
    smtp_port,
    smtp_user,
    smtp_password,
    target_email_address
):
    # Connect
    smtp = smtplib.SMTP_SSL()

    smtp.set_debuglevel(bool(os.getenv('SMTP_DEBUG', None)))

    logging.info('SMTP: connecting to %s:%d', smtp_host, smtp_port)
    smtp.connect(smtp_host, smtp_port)
    logging.info('SMTP: logging in as \'%s\'', smtp_user)
    smtp.login(smtp_user, smtp_password)

    # Get messages...
    can_be_deleted = False
    while True:
        try:
            message_id, lines, msgsize = (yield can_be_deleted)
        except GeneratorExit:
            smtp.quit()
            break

        can_be_deleted = False

        # Extract the right values from the message lines.

        raw_headers = itertools.takewhile(
            lambda line: not line.strip(),
            lines
        )

        headers = MultiDict(
            (match.group(1).title(), match.group(2).strip())
            for match in (HEADER_RE.match(header_line)
                          for header_line in raw_headers)
            if match is not None
        )

        from_address = headers.get('From', None)
        if not from_address:
            logging.debug(
                'SMTP: message %d, missing \'From\' address, skipping',
                message_id
            )
            continue

        try:
            smtp.sendmail(
                from_address,
                target_email_address,
                '\r\n'.join(lines)
            )

        except smtplib.SMTPResponseException as ex:
            logging.error(
                'SMTP: message %d, exception when sending: %s',
                message_id, ex
            )
            continue

        can_be_deleted = True

