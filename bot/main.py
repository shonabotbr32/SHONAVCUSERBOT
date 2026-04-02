#!/usr/bin/env python3
import asyncio
import logging
import signal
import sys
from bot.config import Config
from bot.userbot import VoiceBoostUserbot

# Setup logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('userbot.log')
    ]
)

logger = logging.getLogger(__name__)

# Global userbot instance
userbot = None


def signal_handler(sig, frame):
    """Handle shutdown signals"""
    logger.info("Shutdown signal received...")
    if userbot:
        asyncio.create_task(userbot.stop())
    sys.exit(0)


async def main():
    global userbot

    try:
        # Validate configuration
        Config.validate()

        # Create and start userbot
        userbot = VoiceBoostUserbot()

        logger.info("="*50)
        logger.info("🎤 Telegram Voice Boost Userbot")
        logger.info("="*50)
        logger.info(f"Volume Boost: {Config.VOLUME_BOOST}x")
        logger.info(f"Sample Rate: {Config.SAMPLE_RATE}Hz")
        logger.info("="*50)

        await userbot.start()

        # Keep running
        await asyncio.Event().wait()

    except KeyboardInterrupt:
        logger.info("\n⚠️ Interrupted by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise
    finally:
        if userbot:
            await userbot.stop()


if __name__ == "__main__":
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Run the userbot
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped.")
