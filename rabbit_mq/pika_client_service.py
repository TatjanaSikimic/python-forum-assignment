from typing import List

from rabbit_mq.pika_client import PikaClient

pika_clients : List[PikaClient] = []

def get_pika_client(queue_name):
    # pika_client = next(filter(lambda x: (x.publish_queue_name == queue_name), pika_clients))
    pika_client = None
    for pc in pika_clients:
        if pc.consume_queue_name == queue_name:
            pika_client=pc
            break

    if not pika_client:
        pika_client = PikaClient(queue_name)
    return pika_client