import json

from models import Contact
from rabbitmq import SMS_QUEUE, get_connection


def send_sms(contact):
    print(
        f"[SMS] Повідомлення надіслано: "
        f"{contact.fullname} -> {contact.phone}"
    )


def callback(channel, method, properties, body):
    try:
        data = json.loads(body)
        contact = Contact.objects(id=data["contact_id"]).first()

        if not contact:
            print("Контакт не знайдений.")
            channel.basic_ack(delivery_tag=method.delivery_tag)
            return

        send_sms(contact)
        contact.sent = True
        contact.save()

        channel.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as error:
        print(f"Помилка: {error}")
        channel.basic_nack(
            delivery_tag=method.delivery_tag,
            requeue=False,
        )


def main():
    connection = get_connection()
    channel = connection.channel()

    channel.queue_declare(queue=SMS_QUEUE, durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue=SMS_QUEUE,
        on_message_callback=callback,
    )

    print("SMS consumer запущений...")
    channel.start_consuming()


if __name__ == "__main__":
    main()
