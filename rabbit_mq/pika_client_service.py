from typing import List

import rabbit_mq.pika_client as rabbit_pika_client

pika_clients: List[rabbit_pika_client.PikaClient] = []


def get_pika_client(queue_name):
    pika_client = None
    for pc in pika_clients:
        if pc.consume_queue_name == queue_name:
            pika_client = pc
            break

    if not pika_client:
        pika_client = rabbit_pika_client.PikaClient(queue_name)
    return pika_client
