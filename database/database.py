#(©)CodeXBotz




import pymongo, os
from config import DB_URI, DB_NAME


dbclient = pymongo.MongoClient(DB_URI)
database = dbclient[DB_NAME]


user_data = database['users']
channel_data = database[f'channels{TG_BOT_TOKEN}']
fsub_data = database[f'fsub{TG_BOT_TOKEN}']   
rqst_fsub_data = database[f'request_forcesub{TG_BOT_TOKEN}']
rqst_fsub_Channel_data = database[f'request_forcesub_channel{TG_BOT_TOKEN}']



async def present_user(user_id : int):
    found = user_data.find_one({'_id': user_id})
    return bool(found)

async def add_user(user_id: int):
    user_data.insert_one({'_id': user_id})
    return

async def full_userbase():
    user_docs = user_data.find()
    user_ids = []
    for doc in user_docs:
        user_ids.append(doc['_id'])
        
    return user_ids

async def del_user(user_id: int):
    user_data.delete_one({'_id': user_id})
    return

async def channel_exist(channel_id: int):
    found = await fsub_data.find_one({'_id': channel_id})
    return bool(found)
    
async def add_channel(channel_id: int):
    if not await channel_exist(channel_id):
        await fsub_data.insert_one({'_id': channel_id})
        return

async def rem_channel(channel_id: int):
    if await channel_exist(channel_id):
        await fsub_data.delete_one({'_id': channel_id})
        return

async def show_channels():
    channel_docs = await fsub_data.find().to_list(length=None)
    channel_ids = [doc['_id'] for doc in channel_docs]
    return channel_ids

    
# Get current mode of a channel
async def get_channel_mode(channel_id: int):
    data = await fsub_data.find_one({'_id': channel_id})
    return data.get("mode", "off") if data else "off"

    # Set mode of a channel
async def set_channel_mode(channel_id: int, mode: str):
    await fsub_data.update_one(
        {'_id': channel_id},
        {'$set': {'mode': mode}},
        upsert=True
    )

    # REQUEST FORCE-SUB MANAGEMENT

    # Add the user to the set of users for a   specific channel
async def req_user(channel_id: int, user_id: int):
    try:
        await rqst_fsub_Channel_data.update_one(
            {'_id': int(channel_id)},
            {'$addToSet': {'user_ids': int(user_id)}},
            upsert=True
        )
    except Exception as e:
        print(f"[DB ERROR] Failed to add user to request list: {e}")


    # Method 2: Remove a user from the channel set
async def del_req_user(channel_id: int, user_id: int):
        # Remove the user from the set of users for the channel
    await rqst_fsub_Channel_data.update_one(
        {'_id': channel_id}, 
        {'$pull': {'user_ids': user_id}}
    )

    # Check if the user exists in the set of the channel's users
async def req_user_exist(channel_id: int, user_id: int):
    try:
        found = await rqst_fsub_Channel_data.find_one({
            '_id': int(channel_id),
            'user_ids': int(user_id)
        })
        return bool(found)
    except Exception as e:
        print(f"[DB ERROR] Failed to check request list: {e}")
        return False  


    # Method to check if a channel exists using show_channels
async def reqChannel_exist(channel_id: int):
    # Get the list of all channel IDs from the database 
    channel_ids = await show_channels()
        #print(f"All channel IDs in the database: {channel_ids}")

    # Check if the given channel_id is in the list of channel IDs
    if channel_id in channel_ids:
            #print(f"Channel {channel_id} found in the database.")
        return True
    else:
            #print(f"Channel {channel_id} NOT found in the database.")
        return False

