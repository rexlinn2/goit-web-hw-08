import json
import sys

from faker import Faker

from models import Contact
from rabbitmq import EMAIL_QUEUE, SMS_QUEUE, get_connection

fake = Faker()


def create_contacts(count):
    contacts = []

    for _ in range(count):
        preferred_channel = fake.random_element(
            elements=("email", "sms")
        )

        contact = Contact(
            fullname=fake.name(),
            email=fake.email(),
            phone=fake.phone_number(),
            preferred_channel=preferred_channel,
            sent=False,
        ).save()

        contacts.append(contact)

    return contacts


def publish_contacts(contacts):
    connection = get_connection()
    channel = connection.channel()

    channel.queue_declare(queue=EMAIL_QUEUE, durable=True)
    channel.queue_declare(queue=SMS_QUEUE, durable=True)

    for contact in contacts:
        queue = (
            EMAIL_QUEUE
            if contact.preferred_channel == "email"
            else SMS_QUEUE
        )

        channel.basic_publish(
            exchange="",
            routing_key=queue,
            body=json.dumps({"contact_id": str(contact.id)}),
            properties=None,
        )

        print(
            f"Contact {contact.fullname} -> {queue} "
            f"(id={contact.id})"
        )

    connection.close()


def main():
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 10

    contacts = create_contacts(count)
    publish_contacts(contacts)

    print(f"Створено та поставлено в черги {len(contacts)} контактів.")


if __name__ == "__main__":
    main()
