from django.conf import settings
from django.utils import timezone

from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest


async def parse(client, channel_name, last_parsed_id, limit):
    await client.start()

    channel = await client.get_entity(channel_name)

    parsed_messages = []
    parsed_ids      = []

    history = await client(GetHistoryRequest(
        peer        = channel,
        offset_id   = 0,
        offset_date = None,
        add_offset  = 0,
        limit       = limit,
        max_id      = 0,
        min_id      = last_parsed_id,
        hash        = 0
    ))

    for message in history.messages:
        parsed_ids.append(message.id)
        if message.message and message.id > last_parsed_id: # and not message.fwd_from: #TODO Redundant if?
            parsed_messages.append({
                'text':        message.message,
                'post_id':     message.id,
                'time_posted': message.date,
                'time_parsed': timezone.now(),
            })

    if len(parsed_ids) > 0:
        return parsed_messages, min(parsed_ids), max(parsed_ids)
    else:
        return parsed_messages, last_parsed_id, last_parsed_id


def parse_telegram_channel(channel_name, last_parsed_id, limit):
    
    client = TelegramClient('anon', settings.TELEGRAM_API_ID, settings.TELEGRAM_API_HASH)
    
    with client:
        parsed_messages, new_min_id, new_max_id = client.loop.run_until_complete(parse(client, channel_name, last_parsed_id, limit))

    return parsed_messages, new_min_id, new_max_id
