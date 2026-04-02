import logging
import asyncio
from typing import Dict
from pyrogram import Client
from pytgcalls import PyTgCalls, StreamType
from pytgcalls.types import AudioParameters, MediaStream
from pytgcalls.exceptions import AlreadyJoinedError, NotInCallError
from bot.config import Config
from bot.audio_processor import AudioProcessor

logger = logging.getLogger(__name__)

class VoiceHandler:
    def __init__(self, client: Client):
        self.client = client
        self.pytgcalls = PyTgCalls(client)
        self.audio_processor = AudioProcessor()
        self.active_calls: Dict[int, bool] = {}
        self.setup_handlers()

    def setup_handlers(self):
        @self.pytgcalls.on_stream_end()
        async def on_stream_end(client, update):
            chat_id = update.chat_id
            logger.info(f"Stream ended in chat {chat_id}")
            if chat_id in self.active_calls:
                del self.active_calls[chat_id]

    async def join_voice_chat(self, chat_id: int):
        """Join voice chat with boosted microphone"""
        try:
            if not self.pytgcalls.is_connected:
                await self.pytgcalls.start()

            if chat_id in self.active_calls:
                raise AlreadyJoinedError("Already in this voice chat")

            audio_stream = self.audio_processor.get_boosted_stream()

            await self.pytgcalls.join_group_call(
                chat_id,
                MediaStream(
                    audio_stream,
                    AudioParameters(
                        bitrate=128000,
                    ),
                ),
                stream_type=StreamType().pulse_stream,
            )

            self.active_calls[chat_id] = True
            logger.info(f"✅ Joined voice chat in {chat_id}")

        except AlreadyJoinedError:
            raise Exception("Pehle se voice chat mein hain")
        except Exception as e:
            logger.error(f"Error joining voice chat: {e}")
            raise

    async def leave_voice_chat(self, chat_id: int):
        """Leave voice chat"""
        try:
            if chat_id not in self.active_calls:
                raise NotInCallError("Voice chat mein nahi hain")

            await self.pytgcalls.leave_group_call(chat_id)

            if chat_id in self.active_calls:
                del self.active_calls[chat_id]

            logger.info(f"👋 Left voice chat in {chat_id}")

        except NotInCallError:
            raise Exception("Voice chat mein nahi hain")
        except Exception as e:
            logger.error(f"Error leaving voice chat: {e}")
            raise

    async def update_boost_level(self, boost_level: float):
        """Update volume boost level for active calls"""
        Config.VOLUME_BOOST = boost_level
        Config.FFMPEG_FILTERS = f"volume={boost_level},highpass=f=200"
        logger.info(f"Updated boost level to {boost_level}x")

    def get_status(self) -> str:
        """Get current status"""
        if not self.active_calls:
            return "❌ Kisi bhi voice chat mein nahi hain\n\nCommands..."

        status = f"✅ Active Voice Chats: {len(self.active_calls)}\n"
        status += f"🔊 Volume Boost: {Config.VOLUME_BOOST}x\n"
        status += f"🎧 Sample Rate: {Config.SAMPLE_RATE}Hz\n"
        status += f"📡 Channels: {Config.CHANNELS}\n\n"
        status += "Active Chats:\n"

        for chat_id in self.active_calls.keys():
            status += f"• {chat_id}\n"

        return status

    async def cleanup(self):
        """Cleanup all active calls"""
        for chat_id in list(self.active_calls.keys()):
            try:
                await self.leave_voice_chat(chat_id)
            except:
                pass

        if self.pytgcalls.is_connected:
            await self.pytgcalls.stop()
