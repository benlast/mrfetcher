from .pop3 import process_pop3_messages
from .smtp import send_smtp_messages

def forward(
    pop3_host,
    pop3_port,
    pop3_user,
    pop3_password,
    smtp_host,
    smtp_port,
    smtp_user,
    smtp_password,
    target_email_address
):
    smtp_sender = send_smtp_messages(
        smtp_host,
        smtp_port,
        smtp_user,
        smtp_password,
        target_email_address
    )

    # Start the pop3 producer
    process_pop3_messages(
        pop3_host,
        pop3_port,
        pop3_user,
        pop3_password,
        smtp_sender
    )
