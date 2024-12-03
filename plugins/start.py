#(©)Codeflix_Bots



import os
import asyncio
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated

from bot import Bot
from config import ADMINS, FORCE_MSG, START_MSG, CUSTOM_CAPTION, DISABLE_CHANNEL_BUTTON, PROTECT_CONTENT
from helper_func import subscribed, encode, decode, get_messages
from database.database import add_user, del_user, full_userbase, present_user



@Bot.on_message(filters.command('start') & filters.private & subscribed)
async def start_command(client: Client, message: Message):
    id = message.from_user.id
    if not await present_user(id):
        try:
            await add_user(id)
        except:
            pass
    text = message.text
    if len(text)>7:
        try:
            base64_string = text.split(" ", 1)[1]
        except:
            return
        string = await decode(base64_string)
        argument = string.split("-")
        if len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
            except:
                return
            if start <= end:
                ids = range(start,end+1)
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
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            except:
                return
        temp_msg = await message.reply("ᴡᴀɪᴛ ʙʀᴏᴏ...")
        try:
            messages = await get_messages(client, ids)
        except:
            await message.reply_text("ɪ ꜰᴇᴇʟ ʟɪᴋᴇ ᴛʜᴇʀᴇ ɪꜱ ꜱᴏᴍᴇᴛʜɪɴɢ ᴡʀᴏɴɢ..!")
            return
        await temp_msg.delete()

        snt_msgs = []

        for msg in messages:
            if bool(CUSTOM_CAPTION) & bool(msg.document):
                caption = CUSTOM_CAPTION.format(previouscaption="" if not msg.caption else msg.caption.html, filename=msg.document.file_name)
            else:
                caption = "" if not msg.caption else msg.caption.html

            if DISABLE_CHANNEL_BUTTON:
                reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("𝗠𝗢𝗥𝗘 𝗪𝗘𝗕𝗦𝗜𝗧𝗘𝗦", url='https://t.me/HIDDEN_OFFICIALS_3/3')]])
            else:
                reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("𝗠𝗢𝗥𝗘 𝗪𝗘𝗕𝗦𝗜𝗧𝗘𝗦", url='https://t.me/HIDDEN_OFFICIALS_3/3')]])

            try:
                snt_msg = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                await asyncio.sleep(0.5)
                snt_msgs.append(snt_msg)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                snt_msg = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                snt_msgs.append(snt_msg)
            except:
                pass

        SD = await message.reply_text("‼️ Watch Fast Lectures and Notes before Deleted after 5Hours.\n\nIf Your Lecture Pdf Deleted Don't worry you again able to access 🥰\n\n Go back from where you got link and again click on link and get Again\n\n𝐒𝐨𝐫𝐫𝐲,𝐅𝐨𝐫 𝐭𝐡𝐢𝐬 𝐍𝐨𝐭 𝐅𝐨𝐫𝐰𝐚𝐫𝐝𝐢𝐧𝐠 𝐨𝐧 𝐚𝐧𝐝 𝐧𝐨𝐭 𝐟𝐨𝐫 𝐚 𝐟𝐮𝐥𝐥 𝐭𝐢𝐦𝐞 𝐛𝐜𝐳 𝐰𝐞 𝐠𝐨𝐭 𝐜𝐨𝐩𝐲𝐫𝐢𝐠𝐡𝐭𝐬 😖😖 🙏")
        await asyncio.sleep(18000)

        for snt_msg in snt_msgs:
            try:
               await snt_msg.delete()
               await SD.delete()
            except:
                pass
        return
    else:
        reply_markup = InlineKeyboardMarkup(
            [[
            InlineKeyboardButton("𝗝𝗢𝗜𝗡 𝗢𝗨𝗥 𝗡𝗘𝗪 𝗔𝗗𝗗𝗟𝗜𝗦𝗧 🙏", url="https://t.me/addlist/0W1WED6AnkI4Zjg9")
            ],[
            InlineKeyboardButton("𝐀𝐏𝐍𝐈 𝐊𝐀𝐊𝐒𝐇𝐀 𝐁𝐎𝐓 😈", url="https://t.me/HIDDEN_LEAKED_BOT")
            ],[
            InlineKeyboardButton("Team Hidden", url="https://t.me/HIDDEN_OFFICIALS_1"),
            InlineKeyboardButton("ᴛᴇsᴛ sᴇʀɪᴇs", url="https://t.me/+Fpzh5FbKcoNhZGZl")
            ]]
        )
        await message.reply_text(
            text = START_MSG.format(
                first = message.from_user.first_name,
                last = message.from_user.last_name,
                username = None if not message.from_user.username else '@' + message.from_user.username,
                mention = message.from_user.mention,
                id = message.from_user.id
            ),
            reply_markup = reply_markup,
            disable_web_page_preview = True,
            quote = True
        )
        return   


#=====================================================================================##

WAIT_MSG = "<b>ᴡᴏʀᴋɪɴɢ....</b>"

REPLY_ERROR = "<code>Use this command as a reply to any telegram message without any spaces.</code>"

#=====================================================================================##

    
    
@Bot.on_message(filters.command('start') & filters.private)
async def not_joined(client: Client, message: Message):
    buttons = [
        [
            InlineKeyboardButton(text="JOIN 1st 👍", url=client.invitelink2),
            InlineKeyboardButton(text="Join 2nd 😁", url=client.invitelink3),
        ],
        [
            InlineKeyboardButton(text="JOIN 3rd CHANNEL 👻", url=client.invitelink),
        ]
    ]
    try:
        buttons.append(
            [
                InlineKeyboardButton(
                    text = '• ɴᴏᴡ ᴄʟɪᴄᴋ ʜᴇʀᴇ •',
                    url = f"https://t.me/{client.username}?start={message.command[1]}"
                )
            ]
        )
    except IndexError:
        pass

    await message.reply(
        text = FORCE_MSG.format(
                first = message.from_user.first_name,
                last = message.from_user.last_name,
                username = None if not message.from_user.username else '@' + message.from_user.username,
                mention = message.from_user.mention,
                id = message.from_user.id
            ),
        reply_markup = InlineKeyboardMarkup(buttons),
        quote = True,
        disable_web_page_preview = True
    )

@Bot.on_message(filters.command('users') & filters.private & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
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
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()
