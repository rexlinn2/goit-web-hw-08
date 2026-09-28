import json

from models import Contact
from rabbitmq import EMAIL_QUEUE, get_connection


def send_email(contact):
    # Функція-заглушка: імітує відправлення email.
    print(
        f"[EMAIL] Повідомлення надіслано: "
        f"{contact.fullname} <{contact.email}>"
    )


def callback(channel, method, properties, body):
    try:
        data = json.loads(body)
        contact = Contact.objects(id=data["contact_id"]).first()

        if not contact:
            print("Контакт не знайдений.")
            channel.basic_ack(delivery_tag=method.delivery_tag)
            return

        send_email(contact)
        contact.sent = True
        contact.save()

        channel.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as error:
        print(f"Помилка обробки: {error}")
        channel.basic_nack(
            delivery_tag=method.delivery_tag,
            requeue=False,
        )


def main():
    connection = get_connection()
    channel = connection.channel()

    channel.queue_declare(queue=EMAIL_QUEUE, durable=True)
    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(
        queue=EMAIL_QUEUE,
        on_message_callback=callback,
    )

    print("Email consumer запущений. Очікування повідомлень...")
    channel.start_consuming()


if __name__ == "__main__":
    main()
