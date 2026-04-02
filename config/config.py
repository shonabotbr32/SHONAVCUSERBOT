import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Telegram API Credentials
    API_ID = os.environ.get("API_ID", "")
    API_HASH = os.environ.get("API_HASH", "")
    SESSION_NAME = os.environ.get("SESSION_NAME", "voice_boost_userbot")

    # Audio Settings
    VOLUME_BOOST = float(os.environ.get("VOLUME_BOOST", "10.0"))
    SAMPLE_RATE = int(os.environ.get("SAMPLE_RATE", "48000"))
    CHANNELS = int(os.environ.get("CHANNELS", "2"))

    # FFmpeg Filters
    FFMPEG_FILTERS = os.environ.get(
        "FFMPEG_FILTERS",
        "volume=10.0,highpass=f=200,lowpass=f=3000,afftdn=nf=-25"
    )

    # Logging
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

    @staticmethod
    def validate():
        if not Config.API_ID or not Config.API_HASH:
            raise ValueError("API_ID and API_HASH must be set in environment variables")
        return True
