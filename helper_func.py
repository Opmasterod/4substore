#(©)CodeFlix_Bots

import base64
import re
import asyncio
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from config import ADMINS
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from pyrogram.errors import FloodWait

async def is_subscribed(filter, client, update):
    """
    Filter to check if a user is subscribed to all force-sub channels.
    """
    if not hasattr(client, 'force_sub_ids') or not client.force_sub_ids:
        return True  # No force-sub channels configured

    user_id = update.from_user.id

    if user_id in ADMINS:
        return True

    member_status = [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER]

    for channel_id in client.force_sub_ids:
        try:
            member = await client.get_chat_member(chat_id=channel_id, user_id=user_id)
            if member.status not in member_status:
                return False
        except UserNotParticipant:
            return False
        except Exception as e:
            print(f"Error checking membership for channel {channel_id}: {e}")
            return False

    return True

async def get_invite_link(client, channel_id):
    """
    Get or generate an invite link for a channel.
    """
    try:
        chat = await client.get_chat(channel_id)
        if chat.invite_link:
            return chat.invite_link
        # Generate a new invite link if none exists (requires admin rights)
        invite = await client.export_chat_invite_link(channel_id)
        return invite
    except Exception as e:
        print(f"Error generating invite link for {channel_id}: {e}")
        return None

async def encode(string):
    """
    Encode a string to base64 URL-safe format.
    """
    string_bytes = string.encode("ascii")
    base64_bytes = base64.urlsafe_b64encode(string_bytes)
    base64_string = (base64_bytes.decode("ascii")).strip("=")
    return base64_string

async def decode(base64_string):
    """
    Decode a base64 URL-safe string.
    """
    base64_string = base64_string.strip("=")
    base64_bytes = (base64_string + "=" * (-len(base64_string) % 4)).encode("ascii")
    string_bytes = base64.urlsafe_b64decode(base64_bytes)
    string = string_bytes.decode("ascii")
    return string

async def get_messages(client, message_ids, channel_ids=None):
    """
    Fetch messages from specified message IDs across multiple channel IDs.
    """
    if channel_ids is None:
        channel_ids = getattr(client, 'db_channel_ids', []) or [client.db_channel.id]

    messages = []
    for channel_id in channel_ids:
        total_messages = 0
        while total_messages != len(message_ids):
            temp_ids = message_ids[total_messages:total_messages + 200]
            try:
                msgs = await client.get_messages(
                    chat_id=channel_id,
                    message_ids=temp_ids
                )
            except FloodWait as e:
                await asyncio.sleep(e.x)
                msgs = await client.get_messages(
                    chat_id=channel_id,
                    message_ids=temp_ids
                )
            except Exception as e:
                print(f"Error fetching messages from channel {channel_id}: {e}")
                continue
            total_messages += len(temp_ids)
            messages.extend([msg for msg in msgs if msg is not None])
    return messages

async def get_message_id(client, message):
    """
    Extract message ID from a forwarded message or a Telegram link, checking multiple database channels.
    """
    db_channel_ids = getattr(client, 'db_channel_ids', []) or [client.db_channel.id]

    if message.forward_from_chat:
        if message.forward_from_chat.id in db_channel_ids:
            return message.forward_from_message_id
        else:
            return 0
    elif message.forward_sender_name:
        return 0
    elif message.text:
        pattern = "https://t.me/(?:c/)?(.*)/(\d+)"
        matches = re.match(pattern, message.text)
        if not matches:
            return 0
        channel_id = matches.group(1)
        msg_id = int(matches.group(2))
        if channel_id.isdigit():
            if f"-100{channel_id}" in [str(id) for id in db_channel_ids]:
                return msg_id
        else:
            for db_channel_id in db_channel_ids:
                chat = await client.get_chat(db_channel_id)
                if chat.username and channel_id == chat.username:
                    return msg_id
    return 0

def get_readable_time(seconds: int) -> str:
    """
    Convert seconds to a human-readable time format.
    """
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    hmm = len(time_list)
    for x in range(hmm):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        up_time += f"{time_list.pop()}, "
    time_list.reverse()
    up_time += ":".join(time_list)
    return up_time

subscribed = filters.create(is_subscribed)
