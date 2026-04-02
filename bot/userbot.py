import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from bot.config import Config
from bot.voice_handler import VoiceHandler

logger = logging.getLogger(__name__)

class VoiceBoostUserbot:
    def __init__(self):
        self.app = Client(
            Config.SESSION_NAME,
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            workdir="."
        )
        self.voice_handler = VoiceHandler(self.app)
        self.setup_handlers()

    def setup_handlers(self):
        @self.app.on_message(filters.command("joinvc", prefixes="."))
        async def join_voice_chat(client: Client, message: Message):
            """Join voice chat with boosted audio"""
            try:
                chat_id = message.chat.id
                await self.voice_handler.join_voice_chat(chat_id)
                await message.edit("✅ Voice Chat join kiya! Voice boosted 🔊")
            except Exception as e:
                await message.edit(f"❌ Error: {str(e)}")
                logger.error(f"Join VC error: {e}")

        @self.app.on_message(filters.command("leavevc", prefixes="."))
        async def leave_voice_chat(client: Client, message: Message):
            """Leave voice chat"""
            try:
                chat_id = message.chat.id
                await self.voice_handler.leave_voice_chat(chat_id)
                await message.edit("👋 Voice Chat leave kar diya")
            except Exception as e:
                await message.edit(f"❌ Error: {str(e)}")
                logger.error(f"Leave VC error: {e}")

        @self.app.on_message(filters.command("vcstatus", prefixes="."))
        async def vc_status(client: Client, message: Message):
            """Check voice chat status"""
            status = self.voice_handler.get_status()
            await message.edit(f"📊 **Voice Chat Status**\n\n{status}")

        @self.app.on_message(filters.command("setboost", prefixes="."))
        async def set_boost(client: Client, message: Message):
            """Set custom volume boost level"""
            try:
                if len(message.command) < 2:
                    await message.edit("Usage: .setboost <level>")
                    return

                boost_level = float(message.command[1])
                if boost_level < 1 or boost_level > 20:
                    await message.edit("⚠️ Boost level 1 se 20 ke beech hona chahiye")
                    return

                Config.VOLUME_BOOST = boost_level
                await self.voice_handler.update_boost_level(boost_level)
                await message.edit(f"✅ Volume boost set: {boost_level}x")

            except ValueError:
                await message.edit("❌ Invalid number")
            except Exception as e:
                await message.edit(f"❌ Error: {str(e)}")

    async def start(self):
        """Start the userbot"""
        await self.app.start()
        me = await self.app.get_me()
        logger.info(f"✅ Userbot started as: {me.first_name}")
        logger.info(f"🔊 Voice boost level: {Config.VOLUME_BOOST}x")
        logger.info("Commands: .joinvc | .leavevc | .vcstatus | .setboost")

    async def stop(self):
        """Stop the userbot"""
        await self.voice_handler.cleanup()
        await self.app.stop()
        logger.info("👋 Userbot stopped")

    def run(self):
        """Run the userbot"""
        self.app.run()
