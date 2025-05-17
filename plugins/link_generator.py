#(©)Codexbotz

import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait

from bot import Bot
from config import ADMINS, CHANNEL_ID, DISABLE_CHANNEL_BUTTON
from helper_func import encode

@Bot.on_message(filters.private & filters.user(ADMINS) & ~filters.command(['start', 'users', 'broadcast', 'batch', 'genlink', 'stats', 'addchanneldb', 'listforcesub', 'removeforcesub', 'addforcesub']))
async def channel_post(client: Client, message: Message):
    reply_text = await message.reply_text("Please Wait...!", quote=True)
    
    # Get the list of database channel IDs (fallback to default if empty)
    db_channel_ids = getattr(client, 'db_channel_ids', []) or [client.db_channel.id]
    
    links = []
    post_messages = []
    
    # Copy the message to all database channels
    for channel_id in db_channel_ids:
        try:
            post_message = await message.copy(chat_id=channel_id, disable_notification=True)
            post_messages.append((channel_id, post_message))
        except FloodWait as e:
            await asyncio.sleep(e.x)
            post_message = await message.copy(chat_id=channel_id, disable_notification=True)
            post_messages.append((channel_id, post_message))
        except Exception as e:
            print(f"Error copying message to channel {channel_id}: {e}")
            continue
    
    if not post_messages:
        await reply_text.edit_text("Failed to copy message to any database channel!")
        return
    
    # Generate links for each posted message
    for channel_id, post_message in post_messages:
        converted_id = post_message.id * abs(channel_id)
        string = f"get-{converted_id}"
        base64_string = await encode(string)
        link = f"https://telegram.me/{client.username}?start={base64_string}"
        links.append(f"Channel {channel_id}: <code>{link}</code>")
        
        # Add share button to the channel message if not disabled
        if not DISABLE_CHANNEL_BUTTON:
            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])
            try:
                await post_message.edit_reply_markup(reply_markup)
            except Exception as e:
                print(f"Error adding share button to message in channel {channel_id}: {e}")
    
    # Update the reply with all generated links
    await reply_text.edit(
        f"<b>Here are your links:</b>\n\n" + "\n".join(links),
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URLs", url=f'https://telegram.me/share/url?url={"%0A".join(links)}')]]),
        disable_web_page_preview=True
    )

@Bot.on_message(filters.channel & filters.incoming)
async def new_post(client: Client, message: Message):
    if DISABLE_CHANNEL_BUTTON:
        return
    
    # Get the list of database channel IDs (fallback to default if empty)
    db_channel_ids = getattr(client, 'db_channel_ids', []) or [client.db_channel.id]
    
    # Check if the message is from one of the database channels
    if message.chat.id not in db_channel_ids:
        return
    
    # Generate link for the message
    channel_id = message.chat.id
    converted_id = message.id * abs(channel_id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"https://telegram.me/{client.username}?start={base64_string}"
    
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])
    try:
        await message.edit_reply_markup(reply_markup)
    except Exception as e:
        print(f"Error adding share button to message in channel {channel_id}: {e}")
        pass
