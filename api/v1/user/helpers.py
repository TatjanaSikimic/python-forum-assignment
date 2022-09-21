import datetime
import json
from time import strftime

from api.v1.user.schemas import SendMessage, ReceiveMessage, DisplayUser
from db.models import User


def add_attr(attr_name, attr_value, data, database):
    setattr(data, attr_name, attr_value)
    database.commit()
    database.refresh(data)

    return data


def delete_attr(attr_name, data, database):
    setattr(data, attr_name, None)
    database.commit()
    database.refresh(data)

    return data


def prepare_message_for_sending(content, sender_id, database):
    sender_db = database.query(User).filter(User.id == sender_id).first()

    sender = DisplayUser(username=sender_db.username,
                         avatar=sender_db.avatar,
                         signature=sender_db.signature)

    dt_created = datetime.datetime.now(datetime.timezone.utc)
    message_to_send = ReceiveMessage(dt_created=dt_created.strftime("%d-%b-%Y (%H:%M:%S.%f)"),
                                     content=content,
                                     user=sender)


    return message_to_send

def prepare_message_for_receiving(message_json):
    print(message_json)
    receive_message_dict = json.loads(message_json)
    print(receive_message_dict)

    sender = DisplayUser(username=receive_message_dict["user"]["username"],
                         avatar=receive_message_dict["user"]["avatar"],
                         signature=receive_message_dict["user"]["signature"])

    dt_created_str = receive_message_dict["dt_created"]
    # dt_created = datetime.strptime(dt_created_str, '%Y-%m-%dT%H:%M:%S.%f')
    message_to_receive = ReceiveMessage(dt_created=dt_created_str,
                                     content=receive_message_dict["content"],
                                     user=sender)
    return message_to_receive
