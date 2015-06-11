import collections
import os
import sys

from .forwarder import forward

ENV_VARS = [
    ('POP3_HOST', None),
    ('POP3_PORT', 110),
    ('POP3_USER', None),
    ('POP3_PASSWORD', None),
    ('SMTP_HOST', 'smtp.gmail.com'),
    ('SMTP_PORT', 465),
    ('SMTP_USER', None),
    ('SMTP_PASSWORD', None),
    ('TARGET_EMAIL_ADDRESS', None)
]

def main():
    values = collections.OrderedDict(
        (varname, os.getenv(varname, default))
        for varname, default in ENV_VARS
    )

    missing = [
        varname
        for varname, value in values.iteritems()
        if not value
    ]

    if missing:
        sys.stderr.write(
            'Missing environment variable(s): %s\n' % ', '.join(missing)
        )
        sys.exit(1)

    forward(
        **dict(
            (varname.lower(), value)
            for varname, value in values.iteritems()
        )
    )

