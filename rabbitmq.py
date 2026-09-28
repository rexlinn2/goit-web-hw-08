import os

import pika
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    credentials = pika.PlainCredentials(
        os.getenv("RABBITMQ_USER", "guest"),
        os.getenv("RABBITMQ_PASSWORD", "guest"),
    )

    parameters = pika.ConnectionParameters(
        host=os.getenv("RABBITMQ_HOST", "localhost"),
        port=int(os.getenv("RABBITMQ_PORT", "5672")),
        virtual_host=os.getenv("RABBITMQ_VHOST", "/"),
        credentials=credentials,
    )

    return pika.BlockingConnection(parameters)


EMAIL_QUEUE = "contacts_email"
SMS_QUEUE = "contacts_sms"
