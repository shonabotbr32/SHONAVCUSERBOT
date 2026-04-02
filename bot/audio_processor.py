import logging
from bot.config import Config

logger = logging.getLogger(__name__)

class AudioProcessor:
    def __init__(self):
        self.boost_level = Config.VOLUME_BOOST
        self.sample_rate = Config.SAMPLE_RATE
        self.channels = Config.CHANNELS

    def get_boosted_stream(self) -> str:
        """Get FFmpeg command for boosted audio stream"""
        ffmpeg_filters = Config.FFMPEG_FILTERS

        logger.info(f"Audio filters: {ffmpeg_filters}")
        logger.info(f"Sample rate: {self.sample_rate}Hz, Channels: {self.channels}")

        # Return default device path (Linux PulseAudio)
        return "default"

    def get_filter_chain(self) -> str:
        """Get complete FFmpeg filter chain"""
        filters = []

        # Volume boost (10x = +20dB)
        filters.append(f"volume={self.boost_level}")

        # High-pass filter (remove low frequency noise)
        filters.append("highpass=f=200")

        # Low-pass filter (remove high frequency noise)
        filters.append("lowpass=f=3000")

        # Noise reduction using FFT denoiser
        filters.append("afftdn=nf=-25")

        # Dynamic range compression
        filters.append("acompressor=threshold=0.089:ratio=9")

        # Normalize audio
        filters.append("loudnorm=I=-16:TP=-1.5:LRA=11")

        return ",".join(filters)
