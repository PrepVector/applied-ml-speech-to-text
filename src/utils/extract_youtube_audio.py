import yt_dlp
from src.logger import ProjectLogger

logger = ProjectLogger().get_logger()


class YouTubeAudioExtractor:
    def __init__(self):
        """
        Initialize the YouTubeAudioExtractor.
        """
        self.download_config = {
            "format": "m4a/bestaudio/best",
            "outtmpl": {"default": "./data/uploaded/youtube_audio.%(ext)s"},
            "cachedir": False,
            "verbose": True,
            # "postprocessors": [
            #     {  # Extract audio using ffmpeg
            #         "key": "FFmpegExtractAudio",
            #         "preferredcodec": "m4a",
            #     }
            # ],
        }

    def extract_audio(self, yt_url):
        """
        Extract audio from a YouTube video and save it as an MP4 file.

        Parameters:
        - url (str): The URL of the YouTube video.

        Raises:
        - Exception: If there is an error during the extraction process.
        """
        logger.info(f"Entered extract_audio() in {self.__class__.__name__} class")
        try:
            with yt_dlp.YoutubeDL(self.download_config) as ydl:
                error_code = ydl.download(yt_url)
        except Exception as e:
            logger.error("Failed to extract audio from YouTube Video")
            logger.exception(e)
        logger.info("Exiting extract_audio()")
