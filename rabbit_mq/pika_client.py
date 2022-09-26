import json
import uuid
import pika
import config


class PikaClient:

    def __init__(self, queue_name):
        self.queue_name = queue_name

    def receive_message(self):
        messages = []
        parameters = pika.ConnectionParameters(host=config.RABBIT_HOST,
                                               port=config.RABBIT_PORT)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.queue_declare(queue=self.queue_name)

        method_frame, header_frame, body = channel.basic_get(queue=self.queue_name)

        while method_frame is not None and method_frame.NAME != 'Basic.GetEmpy':
            method_frame, header_frame, body = channel.basic_get(queue=self.queue_name)
            if body is not None:
                messages.append(body)
        if method_frame is not None and method_frame.NAME != 'Basic.GetEmpy':
            channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        connection.close()
        return messages

    def send_message(self, message):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=config.RABBIT_HOST)
        )
        channel = connection.channel()
        publish_queue = channel.queue_declare(queue=self.queue_name)
        channel.basic_publish(
            exchange='',
            routing_key=self.queue_name,
            properties=pika.BasicProperties(
                correlation_id=str(uuid.uuid4())
            ),

            body=json.dumps(message)

        )
        connection.close()
