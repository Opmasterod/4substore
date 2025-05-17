#(©)AnimeXyz

from aiohttp import web
from plugins import web_server

import pyromod.listen
from pyrogram import Client
from pyrogram.enums import ParseMode
import sys
from datetime import datetime

from config import API_HASH, APP_ID, LOGGER, TG_BOT_TOKEN, TG_BOT_WORKERS, CHANNEL_ID, PORT

name = """
 BY MIKEY FROM TG
"""

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Bot",
            api_hash=API_HASH,
            api_id=APP_ID,
            plugins={
                "root": "plugins"
            },
            workers=TG_BOT_WORKERS,
            bot_token=TG_BOT_TOKEN
        )
        self.LOGGER = LOGGER
        # Initialize lists for force-sub and database channels
        self.force_sub_ids = []
        self.force_sub_links = {}  # Dictionary to store channel ID -> invite link
        self.db_channel_ids = []

    async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()
        self.uptime = datetime.now()

        # Initialize default database channel
        try:
            db_channel = await self.get_chat(CHANNEL_ID)
            self.db_channel = db_channel
            test = await self.send_message(chat_id=db_channel.id, text="Test Message")
            await test.delete()
            self.db_channel_ids = [CHANNEL_ID]  # Default channel
            self.LOGGER(__name__).info(f"Default database channel validated: {CHANNEL_ID}")
        except Exception as e:
            self.LOGGER(__name__).warning(e)
            self.LOGGER(__name__).warning(f"Make sure bot is Admin in DB Channel, and double check the CHANNEL_ID value, Current Value: {CHANNEL_ID}")
            self.LOGGER(__name__).info("\nBot Stopped. Join https://t.me/weebs_support for support")
            sys.exit()

        # Load additional database and force-sub channels (e.g., from database or config)
        # Note: Actual loading depends on your database implementation
        # For now, we'll assume they're set via commands in the main bot code
        self.db_channel_ids = getattr(self, 'db_channel_ids', [CHANNEL_ID])
        self.force_sub_ids = getattr(self, 'force_sub_ids', [])
        self.force_sub_links = getattr(self, 'force_sub_links', {})

        # Validate and generate invite links for force-sub channels
        for channel_id in self.force_sub_ids:
            try:
                link = (await self.get_chat(channel_id)).invite_link
                if not link:
                    link = await self.export_chat_invite_link(channel_id)
                self.force_sub_links[channel_id] = link
                self.LOGGER(__name__).info(f"Invite link for force-sub channel {channel_id}: {link}")
            except Exception as e:
                self.LOGGER(__name__).warning(e)
                self.LOGGER(__name__).warning(f"Bot can't export invite link for force-sub channel {channel_id}. Ensure bot is admin with Invite Users via Link permission.")
                self.force_sub_ids.remove(channel_id)  # Remove invalid channel
                self.force_sub_links.pop(channel_id, None)

        # Validate additional database channels
        for channel_id in self.db_channel_ids:
            if channel_id == CHANNEL_ID:
                continue  # Already validated
            try:
                db_channel = await self.get_chat(channel_id)
                test = await self.send_message(chat_id=db_channel.id, text="Test Message")
                await test.delete()
                self.LOGGER(__name__).info(f"Database channel validated: {channel_id}")
            except Exception as e:
                self.LOGGER(__name__).warning(e)
                self.LOGGER(__name__).warning(f"Failed to validate database channel {channel_id}. Ensure bot is admin.")
                self.db_channel_ids.remove(channel_id)

        self.set_parse_mode(ParseMode.HTML)
        self.LOGGER(__name__).info(f"Bot Running..!\n\nCreated by \nhttps://t.me/weebs_support")
        self.LOGGER(__name__).info(f"""
  ___ ___  ___  ___ ___ _    _____  _____  ___ _____ ___ 
 / __/ _ \|   \| __| __| |  |_ _\ \/ / _ )/ _ \_   _/ __|
| (_| (_) | |) | _|| _|| |__ | | >  <| _ \ (_) || | \__ \
 \___\___/|___/|___|_| |____|___/_/\_\___/\___/ |_| |___/
                                                         
""")
        self.username = usr_bot_me.username
        # Web response
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, PORT).start()

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped.")
