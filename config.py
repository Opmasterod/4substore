#(©)t.me/CodeFlix_Bots




import os
import logging
from logging.handlers import RotatingFileHandler
from pymongo import MongoClient


#Bot token @Botfather
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")

#Your API ID from my.telegram.org
APP_ID = int(os.environ.get("APP_ID", "23713783"))

#Your API Hash from my.telegram.org
API_HASH = os.environ.get("API_HASH", "2daa157943cb2d76d149c4de0b036a99")

#Your db channel Id
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1001995978690"))

# NAMA OWNER
OWNER = os.environ.get("OWNER", "ll_HACKHEIST_ll")

#OWNER ID
OWNER_ID = int(os.environ.get("OWNER_ID", "5487643307"))

#Port
PORT = os.environ.get("PORT", "8030")

#Database
DB_URI = os.environ.get("DATABASE_URL", "mongodb+srv://namanjain123eudhc:opmaster@cluster0.5iokvxo.mongodb.net/?retryWrites=true&w=majority")
DB_NAME = os.environ.get("DATABASE_NAME", "Cluster0")

mongo_client = MongoClient(DB_URI)
mongo_db = mongo_client[DB_NAME]

# Add this line for access control collection
access_collection = mongo_db["access_users"]
refer_collection = mongo_db["refer"]

#force sub channel id, if you want enable force sub
FORCESUB_CHANNEL = int(os.environ.get("FORCESUB_CHANNEL", "-1001473043276"))
FORCESUB_CHANNEL2 = int(os.environ.get("FORCESUB_CHANNEL2", "-1001644866777"))
FORCESUB_CHANNEL3 = int(os.environ.get("FORCESUB_CHANNEL3", "-1001473043276"))

TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "4"))

FILE_AUTO_DELETE = int(os.getenv("FILE_AUTO_DELETE", "28800")) # auto delete in seconds

#start message
START_MSG = os.environ.get("START_MESSAGE", "Hey , {first}\n\nThanks to come here ❤️\n\nI am HACKHEIST helper to help in stuidies if you are serious aspriant then you are on right place 👍\n\n<b>Credit - @HIDDEN_OFFICIALS_5</b>")
try:
    ADMINS=[5487643307]
    for x in (os.environ.get("ADMINS", "").split()):
        ADMINS.append(int(x))
except ValueError:
        raise Exception("Your Admins list does not contain valid integers.")

#Force sub message 
FORCE_MSG = os.environ.get("FORCE_SUB_MESSAGE", "<b>Hey , {first}\n\n<b>Bro/Sister first of all you have to join our 3 channels using below buttons click on button join channels one by one and then click on NOW CLICK HERE button</b>\n\nYou have to do it only 1 time 😍 \n\nAny problem - @HACKHEISTBOT</b>")

#set your Custom Caption here, Keep None for Disable Custom Caption
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", """<b>{previouscaption}</b>\n<b>━━━━━━━━━━━━━━━━━◇</b>\n<b>⛧ 🄱🅈 :-) </b><b><a href="https://yashyasag.github.io/hiddens">ℍ𝔸ℂ𝕂ℍ𝔼𝕀𝕊𝕋 😈</a></b> <b>♛</b>\n<b>━━━━━━━━━━━━━━━━━◇</b>\n<b>🙏 sʜᴀʀᴇ ᴀɴᴅ sᴜᴘᴘᴏʀᴛ ᴜs 👇</b>\n<b>—————————————————</b>\n<b><a href="https://yashyasag.github.io/hiddens">🚀 𝗠𝗢𝗥𝗘 𝗪𝗘𝗕𝗦𝗜𝗧𝗘𝗦 🌟</a></b>\n<b>—————————————————</b>""")

#set True if you want to prevent users from forwarding files from bot
PROTECT_CONTENT = True if os.environ.get('PROTECT_CONTENT', "False") == "True" else False

#Set true if you want Disable your Channel Posts Share button
DISABLE_CHANNEL_BUTTON = os.environ.get("DISABLE_CHANNEL_BUTTON", None) == 'True'

BOT_STATS_TEXT = "<b>BOT UPTIME</b>\n{uptime}"
USER_REPLY_TEXT = "ʙᴀᴋᴋᴀ ! ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴍʏ ꜱᴇɴᴘᴀɪ!!"



ADMINS.append(OWNER_ID)
ADMINS.append(5487643307)
ALLOWED_USERS = [7137002799]


LOG_FILE_NAME = "filesharingbot.txt"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
   
