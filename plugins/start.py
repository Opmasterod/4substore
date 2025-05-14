#(©)Codeflix_Bots

import random
import os
import asyncio
import humanize
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated
from config import FILE_AUTO_DELETE, ADMINS, FORCE_MSG, START_MSG, CUSTOM_CAPTION, DISABLE_CHANNEL_BUTTON, PROTECT_CONTENT
from helper_func import subscribed, encode, decode, get_messages, get_invite_link
from database.database import add_user, del_user, full_userbase, present_user

# Initialize lists for database and force-sub channels
DB_CHANNEL_IDS = []
FORCE_SUB_IDS = []
FORCE_SUB_LINKS = {}  # Dictionary to store channel ID -> invite link mapping

codeflixbots = FILE_AUTO_DELETE
subaru = codeflixbots
file_auto_delete = humanize.naturaldelta(subaru)

# Command to add multiple database channel IDs
@Bot.on_message(filters.command('addchanneldb') & filters.private & filters.user(ADMINS))
async def add_channel_db(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply("Please provide channel IDs in the format: /addchanneldb -100928472847,-100385858283")
        return
    
    channel_ids = message.command[1].split(",")
    valid_ids = []
    
    for channel_id in channel_ids:
        try:
            channel_id = channel_id.strip()
            if not channel_id.startswith("-100"):
                await message.reply(f"Invalid channel ID: {channel_id}. Channel IDs must start with -100.")
                continue
            channel_id = int(channel_id)
            await client.get_chat(channel_id)
            valid_ids.append(channel_id)
        except ValueError:
            await message.reply(f"Invalid channel ID: {channel_id}. Please provide valid numeric IDs.")
        except Exception as e:
            await message.reply(f"Error accessing channel {channel_id}: {str(e)}")
    
    if valid_ids:
        global DB_CHANNEL_IDS
        DB_CHANNEL_IDS.extend([id for id in valid_ids if id not in DB_CHANNEL_IDS])
        client.db_channel_ids = DB_CHANNEL_IDS
        await message.reply(f"Added {len(valid_ids)} channel(s) to the database: {', '.join(str(id) for id in valid_ids)}\nCurrent database channels: {', '.join(str(id) for id in DB_CHANNEL_IDS)}")
    else:
        await message.reply("No valid channel IDs were added.")

# Command to add multiple force-sub channel IDs
@Bot.on_message(filters.command('addforcesub') & filters.private & filters.user(ADMINS))
async def add_force_sub(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply("Please provide channel IDs in the format: /addforcesub -10029482733,-10038583833")
        return
    
    channel_ids = message.command[1].split(",")
    valid_ids = []
    
    for channel_id in channel_ids:
        try:
            channel_id = channel_id.strip()
            if not channel_id.startswith("-100"):
                await message.reply(f"Invalid channel ID: {channel_id}. Channel IDs must start with -100.")
                continue
            channel_id = int(channel_id)
            # Verify bot has access and get invite link
            invite_link = await get_invite_link(client, channel_id)
            if not invite_link:
                await message.reply(f"Could not get invite link for channel {channel_id}. Ensure the bot is an admin.")
                continue
            valid_ids.append(channel_id)
            FORCE_SUB_LINKS[channel_id] = invite_link
        except ValueError:
            await message.reply(f"Invalid channel ID: {channel_id}. Please provide valid numeric IDs.")
        except Exception as e:
            await message.reply(f"Error accessing channel {channel_id}: {str(e)}")
    
    if valid_ids:
        global FORCE_SUB_IDS
        FORCE_SUB_IDS.extend([id for id in valid_ids if id not in FORCE_SUB_IDS])
        client.force_sub_ids = FORCE_SUB_IDS
        await message.reply(f"Added {len(valid_ids)} force-sub channel(s): {', '.join(str(id) for id in valid_ids)}\nCurrent force-sub channels: {', '.join(str(id) for id in FORCE_SUB_IDS)}")
    else:
        await message.reply("No valid channel IDs were added.")

# Command to list force-sub channels
@Bot.on_message(filters.command('listforcesub') & filters.private & filters.user(ADMINS))
async def list_force_sub(client: Client, message: Message):
    if not FORCE_SUB_IDS:
        await message.reply("No force-sub channels configured.")
    else:
        await message.reply(f"Current force-sub channels:\n{', '.join(str(id) for id in FORCE_SUB_IDS)}")

# Command to remove a force-sub channel
@Bot.on_message(filters.command('removeforcesub') & filters.private & filters.user(ADMINS))
async def remove_force_sub(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply("Please provide a channel ID to remove: /removeforcesub -10029482733")
        return
    try:
        channel_id = int(message.command[1].strip())
        global FORCE_SUB_IDS, FORCE_SUB_LINKS
        if channel_id in FORCE_SUB_IDS:
            FORCE_SUB_IDS.remove(channel_id)
            FORCE_SUB_LINKS.pop(channel_id, None)
            client.force_sub_ids = FORCE_SUB_IDS
            await message.reply(f"Removed force-sub channel {channel_id}.\nCurrent force-sub channels: {', '.join(str(id) for id in FORCE_SUB_IDS) or 'None'}")
        else:
            await message.reply(f"Channel {channel_id} not found in force-sub channels.")
    except ValueError:
        await message.reply("Invalid channel ID. Please provide a valid numeric ID.")

@Bot.on_message(filters.command('start') & filters.private & subscribed)
async def start_command(client: Client, message: Message):
    id = message.from_user.id
    if not await present_user(id):
        try:
            await add_user(id)
        except:
            pass
    text = message.text
    if len(text) > 7:
        try:
            base64_string = text.split(" ", 1)[1]
        except:
            return
        string = await decode(base64_string)
        argument = string.split("-")
        if len(argument) == 3:
            try:
                channel_id = DB_CHANNEL_IDS[0] if DB_CHANNEL_IDS else client.db_channel.id
                start = int(int(argument[1]) / abs(channel_id))
                end = int(int(argument[2]) / abs(channel_id))
            except:
                return
            if start <= end:
                ids = range(start, end + 1)
            else:
                ids = []
                i = start
                while True:
                    ids.append(i)
                    i -= 1
                    if i < end:
                        break
        elif len(argument) == 2:
            try:
                channel_id = DB_CHANNEL_IDS[0] if DB_CHANNEL_IDS else client.db_channel.id
                ids = [int(int(argument[1]) / abs(channel_id))]
            except:
                return
        temp_msg = await message.reply("Wait A Sec..")
        try:
            messages = await get_messages(client, ids, DB_CHANNEL_IDS or [client.db_channel.id])
        except Exception as e:
            await message.reply_text("Something Went Wrong..!")
            print(f"Error getting messages: {e}")
            return
        finally:
            await temp_msg.delete()

        codeflix_msgs = []

        for msg in messages:
            filename = "Unknown"
            media_type = "Unknown"

            if msg.video:
                media_type = "Video"
                filename = msg.video.file_name if msg.video.file_name else "Unnamed Video"
            elif msg.document:
                filename = msg.document.file_name if msg.document.file_name else "Unnamed Document"
                media_type = "PDF" if filename.endswith(".pdf") else "Document"
            elif msg.photo:
                media_type = "Image"
                filename = "Image"
            elif msg.text:
                media_type = "Text"
                filename = "Text Content"

            caption = (
                CUSTOM_CAPTION.format(
                    previouscaption=(msg.caption.html if msg.caption else msg.file_name or ""),
                    filename=filename,
                    mediatype=media_type,
                )
                if bool(CUSTOM_CAPTION)
                else (msg.caption.html if msg.caption else "")
            )

            reply_markup = msg.reply_markup if not DISABLE_CHANNEL_BUTTON else None

            try:
                copied_msg = await msg.copy(
                    chat_id=message.from_user.id,
                    caption=caption,
                    parse_mode=ParseMode.HTML,
                    reply_markup=reply_markup,
                    protect_content=PROTECT_CONTENT,
                )
                if copied_msg:
                    codeflix_msgs.append(copied_msg)
            except Flood

Wait as e:
                await asyncio.sleep(e.x)
                try:
                    copied_msg = await msg.copy(
                        chat_id=message.from_user.id,
                        caption=caption,
                        parse_mode=ParseMode.HTML,
                        reply_markup=reply_markup,
                        protect_content=PROTECT_CONTENT,
                    )
                    if copied_msg:
                        codeflix_msgs.append(copied_msg)
                except Exception as e:
                    print(f"Failed to send message after waiting: {e}")
            except Exception as e:
                print(f"Failed to send message: {e}")
                
        k = await client.send_message(
            chat_id=message.from_user.id,
            text=f"<b>𝗕𝘂𝗱𝗱𝘆 𝘆𝗼𝘂𝗿 𝗿𝗲𝗾𝘂𝗲𝘀𝘁𝗲𝗱 𝗺𝗮𝘁𝗲𝗿𝗶𝗮𝗹 𝗴𝗼𝗻𝗲 𝗱�_e𝗹𝗲𝘁𝗲 😕 𝗶𝗻 {file_auto_delete}</b>\n\n"
                 f"<b>But Don,t worry 🥰 you again access through my websites 🌟</b>\n\n"
                 f"<b>𝗔𝗹𝗹 𝗖𝗿𝗲𝗱𝗶𝘁𝘀 𝗳𝗼�_r 𝘁𝗵𝗶𝘀 𝗺𝗮𝘁𝗲𝗿𝗶𝗮𝗹 𝗴𝗼𝗲𝘀 𝘁𝗼 ℍ𝔸ℂ𝕂ℍ𝔼𝕀𝕊𝕋 😈</b>",
        )

        codeflix_msgs.append(k)

        special_msg_ids = [44219, 44224, 44225, 44226, 44227, 44228, 44229, 44230, 44231, 44232, 44234, 44235, 44237, 44238, 44240, 44242, 44243, 44244, 44245, 44247, 44248, 44249, 44250, 44251, 44253, 44254, 44255, 44256, 44257, 44258, 44259, 44260, 44261, 44262, 44263, 44264, 44265, 44266, 44267, 44268]

        random_msg_id = random.choice(special_msg_ids)

        try:
            channel_id = DB_CHANNEL_IDS[0] if DB_CHANNEL_IDS else client.db_channel.id
            special_msg = await client.get_messages(channel_id, random_msg_id)

            if not special_msg:
                await client.send_message(chat_id=message.from_user.id, text="⚠️ Special message not found!")
            else:
                if special_msg.sticker:
                    special_copied_msg = await client.send_sticker(
                        chat_id=message.from_user.id,
                        sticker=special_msg.sticker.file_id
                    )
                else:
                    await client.send_message(chat_id=message.from_user.id, text="⚠️ Unsupported message type!")
        except Exception as e:
            await client.send_message(chat_id=message.from_user.id, text=f"Error: {str(e)}")
            print(f"Failed to fetch special message: {e}")

        asyncio.create_task(delete_files(codeflix_msgs, client, k))
        return
    else:
        reply_markup = InlineKeyboardMarkup(
            [[
                InlineKeyboardButton("𝗠𝗔𝗜𝗡 𝗪𝗘𝗕𝗦𝗜𝗧𝗘 😁", url="https://t.me/HIDDEN_OFFgoogle3/3")
            ], [
                InlineKeyboardButton("𝐀𝐏𝐍𝐈 𝐊𝐀𝐊𝐒𝐇𝐀 𝗪𝗘𝗕𝗦𝗜𝗧𝗘 😱", url="https://yashyasag.github.io/tesetoss")
            ], [
                InlineKeyboardButton("MIT SCHOOL 😁", url="https://mits-ak.github.io/mitbyhh/")
            ]]
        )
        await message.reply_text(
            text=START_MSG.format(
                first=message.from_user.first_name,
                last=message.from_user.last_name,
                username=None if not message.from_user.username else '@' + message.from_user.username,
                mention=message.from_user.mention,
                id=message.from_user.id
            ),
            reply_markup=reply_markup,
            disable_web_page_preview=True,
            quote=True
        )
        return

# Updated not_joined handler with dynamic buttons
@Bot.on_message(filters.command('start') & filters.private)
async def not_joined(client: Client, message: Message):
    buttons = []
    force_sub_ids = getattr(client, 'force_sub_ids', [])
    
    if not force_sub_ids:
        # Fallback to original channels if no force-sub channels are configured
        buttons = [
            [
                InlineKeyboardButton(text="1st Channel", url=client.invitelink2),
                InlineKeyboardButton(text="2nd Channel", url=client.invitelink3),
            ],
            [
                InlineKeyboardButton(text="3rd channel", url=client.invitelink),
            ]
        ]
    else:
        # Generate buttons dynamically (two per row)
        for i in range(0, len(force_sub_ids), 2):
            row = []
            for j in range(2):
                if i + j < len(force_sub_ids):
                    channel_id = force_sub_ids[i + j]
                    row.append(
                        InlineKeyboardButton(
                            text=f"Join {i + j + 1}",
                            url=FORCE_SUB_LINKS.get(channel_id, "https://t.me/")
                        )
                    )
            buttons.append(row)
    
    # Add "Now try again" button
    try:
        buttons.append(
            [
                InlineKeyboardButton(
                    text='• ɴᴏᴡ ᴛʀʏ ᴀɢᴀɪɴ •',
                    url=f"https://t.me/{client.username}?start={message.command[1] if len(message.command) > 1 else ''}"
                )
            ]
        )
    except IndexError:
        pass

    await message.reply(
        text=FORCE_MSG.format(
            first=message.from_user.first_name,
            last=message.from_user.last_name,
            username=None if not message.from_user.username else '@' + message.from_user.username,
            mention=message.from_user.mention,
            id=message.from_user.id
        ),
        reply_markup=InlineKeyboardMarkup(buttons),
        quote=True,
        disable_web_page_preview=True
    )

@Bot.on_message(filters.command('users') & filters.private & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text="ᴡᴏʀᴋɪɴɢ....")
    users = await full_userbase()
    await msg.edit(f"{len(users)} ᴜꜱᴇʀꜱ ᴀʀᴇ ᴜꜱɪɴɢ ᴛʜɪꜱ ʙᴏᴛ")

@Bot.on_message(filters.private & filters.command('broadcast') & filters.user(ADMINS))
async def send_text(client: Bot, message: Message):
    if message.reply_to_message:
        query = await full_userbase()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0
        
        pls_wait = await message.reply("<i>ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴘʀᴏᴄᴇꜱꜱɪɴɢ ᴛɪʟʟ ᴡᴀɪᴛ ʙʀᴏᴏ... </i>")
        for chat_id in query:
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                await del_user(chat_id)
                blocked += 1
            except InputUserDeactivated:
                await del_user(chat_id)
                deleted += 1
            except:
                unsuccessful += 1
                pass
            total += 1
        
        status = f"""<b><u>ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴄᴏᴍᴘʟᴇᴛᴇᴅ ᴍʏ sᴇɴᴘᴀɪ!!</u>

ᴛᴏᴛᴀʟ ᴜꜱᴇʀꜱ: <code>{total}</code>
ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟ: <code>{successful}</code>
ʙʟᴏᴄᴋᴇᴅ ᴜꜱᴇʀꜱ: <code>{blocked}</code>
ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛꜱ: <code>{deleted}</code>
ᴜɴꜱᴜᴄᴄᴇꜱꜱꜰᴜʟ: <code>{unsuccessful}</code></b></b>"""
        
        return await pls_wait.edit(status)

    else:
        msg = await message.reply("<code>Use this command as a reply to any telegram message without any spaces.</code>")
        await asyncio.sleep(8)
        await msg.delete()

async def delete_files(messages, client, k=None):
    """
    Delete messages after the specified auto-delete duration.
    """
    await asyncio.sleep(FILE_AUTO_DELETE)
    
    for msg in messages:
        try:
            await client.delete_messages(chat_id=msg.chat.id, message_ids=[msg.id])
        except Exception as e:
            print(f"The attempt to delete the media {msg.id} was unsuccessful: {e}")

    if k:
        command_part = k.command[1] if k.command and len(k.command) > 1 else None
        if command_part:
            button_url = f"https://t.me/{client.username}?start={command_part}"
            keyboard = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("ɢᴇᴛ ғɪʟᴇ ᴀɢᴀɪɴ!", url=button_url)]
                ]
            )
        else:
            keyboard = None

        try:
            await k.edit_text("<b><i>Your Video / File Is Successfully Deleted ✅</i></b>", reply_markup=keyboard)
        except Exception as e:
            print(f"Failed to edit deletion message: {e}")
