from pyrogram import Client, filters
from pyrogram.types import Message
from datetime import datetime, timedelta
from config import access_collection, ADMINS

# /adduser <user_id> <minutes>
@Bot.on_message(filters.command("adduser") & filters.private & filters.user(ADMINS))
async def add_user_cmd(client: Client, message: Message):
    args = message.text.split()
    if len(args) != 3:
        return await message.reply("Usage:\n`/adduser <user_id> <minutes>`", quote=True)
    
    try:
        user_id = int(args[1])
        minutes = int(args[2])
    except ValueError:
        return await message.reply("User ID and minutes must be numbers.")

    now = datetime.utcnow()
    expiry = now + timedelta(minutes=minutes)

    access_collection.update_one(
        {"user_id": user_id},
        {"$set": {
            "user_id": user_id,
            "joined_at": now,
            "expires_at": expiry
        }},
        upsert=True
    )

    await message.reply(f"✅ User `{user_id}` added with access for `{minutes}` minutes.")

# /removeuser <user_id>
@Bot.on_message(filters.command("removeuser") & filters.private & filters.user(ADMINS))
async def remove_user_cmd(client: Client, message: Message):
    args = message.text.split()
    if len(args) != 2:
        return await message.reply("Usage:\n`/removeuser <user_id>`", quote=True)
    
    try:
        user_id = int(args[1])
    except ValueError:
        return await message.reply("User ID must be a number.")

    result = access_collection.delete_one({"user_id": user_id})

    if result.deleted_count:
        await message.reply(f"✅ User `{user_id}` removed.")
    else:
        await message.reply("❌ User not found.")

# /listusers
@Bot.on_message(filters.command("listusers") & filters.private & filters.user(ADMINS))
async def list_users_cmd(client: Client, message: Message):
    users = access_collection.find()
    if access_collection.count_documents({}) == 0:
        return await message.reply("No users found.")

    msg = "<b>Allowed Users:</b>\n\n"
    for user in users:
        uid = user["user_id"]
        joined = user["joined_at"].strftime("%Y-%m-%d %H:%M")
        expires = user["expires_at"].strftime("%Y-%m-%d %H:%M")
        msg += f"• <code>{uid}</code>\n  Joined: {joined}\n  Expires: {expires}\n\n"

    await message.reply_text(msg, parse_mode="html")
