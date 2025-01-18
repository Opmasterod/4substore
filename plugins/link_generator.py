from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot import Bot
from config import ADMINS
from helper_func import encode, get_message_id

@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('batch'))
async def batch(client: Client, message: Message):
    # Process for db_channel1
    while True:
        try:
            first_message1 = await client.ask(
                text="Forward the First Message from DB Channel 1 (with Quotes)..\n\nor Send the DB Channel Post Link",
                chat_id=message.from_user.id,
                filters=(filters.forwarded | (filters.text & ~filters.forwarded)),
                timeout=60
            )
        except:
            return
        f_msg_id1 = await get_message_id(client, first_message1)
        if f_msg_id1:
            break
        else:
            await first_message1.reply(
                "❌ Error\n\nthis Forwarded Post is not from DB Channel 1 or this Link is not valid.",
                quote=True
            )
            continue

    while True:
        try:
            second_message1 = await client.ask(
                text="Forward the Last Message from DB Channel 1 (with Quotes)..\nor Send the DB Channel Post link",
                chat_id=message.from_user.id,
                filters=(filters.forwarded | (filters.text & ~filters.forwarded)),
                timeout=60
            )
        except:
            return
        s_msg_id1 = await get_message_id(client, second_message1)
        if s_msg_id1:
            break
        else:
            await second_message1.reply(
                "❌ Error\n\nthis Forwarded Post is not from DB Channel 1 or this Link is not valid.",
                quote=True
            )
            continue

    # Generate link for db_channel1
    string1 = f"get-{f_msg_id1 * abs(client.db_channel1.id)}-{s_msg_id1 * abs(client.db_channel1.id)}"
    base64_string1 = await encode(string1)
    link1 = f"https://t.me/{client.username}?start={base64_string1}"

    # Send link for db_channel1
    reply_markup1 = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link1}')]])
    await second_message1.reply_text(
        f"<b>Here is your link for DB Channel 1</b>\n\n<code>{link1}</code>",
        quote=True,
        reply_markup=reply_markup1
    )

    # Process for db_channel2
    while True:
        try:
            first_message2 = await client.ask(
                text="Forward the First Message from DB Channel 2 (with Quotes)..\n\nor Send the DB Channel Post Link",
                chat_id=message.from_user.id,
                filters=(filters.forwarded | (filters.text & ~filters.forwarded)),
                timeout=60
            )
        except:
            return
        f_msg_id2 = await get_message_id(client, first_message2)
        if f_msg_id2:
            break
        else:
            await first_message2.reply(
                "❌ Error\n\nthis Forwarded Post is not from DB Channel 2 or this Link is not valid.",
                quote=True
            )
            continue

    while True:
        try:
            second_message2 = await client.ask(
                text="Forward the Last Message from DB Channel 2 (with Quotes)..\nor Send the DB Channel Post link",
                chat_id=message.from_user.id,
                filters=(filters.forwarded | (filters.text & ~filters.forwarded)),
                timeout=60
            )
        except:
            return
        s_msg_id2 = await get_message_id(client, second_message2)
        if s_msg_id2:
            break
        else:
            await second_message2.reply(
                "❌ Error\n\nthis Forwarded Post is not from DB Channel 2 or this Link is not valid.",
                quote=True
            )
            continue

    # Generate link for db_channel2
    string2 = f"get-{f_msg_id2 * abs(client.db_channel2.id)}-{s_msg_id2 * abs(client.db_channel2.id)}"
    base64_string2 = await encode(string2)
    link2 = f"https://t.me/{client.username}?start={base64_string2}"

    # Send link for db_channel2
    reply_markup2 = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link2}')]])
    await second_message2.reply_text(
        f"<b>Here is your link for DB Channel 2</b>\n\n<code>{link2}</code>",
        quote=True,
        reply_markup=reply_markup2
    )
