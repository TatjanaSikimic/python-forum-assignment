import json
import uuid
# from venv import logger

import pika
from aio_pika import connect_robust

import config


class PikaClient:

    def __init__(self, queue_name):
        self.publish_queue_name = queue_name
        self.consume_queue_name = queue_name
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=config.RABBIT_HOST)
        )
        self.channel = self.connection.channel()
        self.publish_queue = self.channel.queue_declare(queue=self.publish_queue_name)
        self.callback_queue = self.publish_queue.method.queue
        self.response = None
        # self.process_callable = process_callable
        print('Pika connection initialized')

    async def consume(self):
        """Setup message listener with the current running loop"""
        connection = await connect_robust(host=config.RABBIT_HOST,
                                          port=config.RABBIT_PORT,
                                          )
        channel = await connection.channel()
        queue = await channel.declare_queue(self.consume_queue_name)
        await queue.consume(self.receive_message, no_ack=False)
        print('Established pika async listener')
        return connection

    async def receive_message(self, message):
        await message.ack()
        body = message.body
        print('Received message')
        if body:
            print(body)

    def send_message(self, message):
        print(message)
        self.channel.basic_publish(
            exchange='',
            routing_key=self.publish_queue_name,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=str(uuid.uuid4())
            ),

            body=json.dumps(message)

        )
