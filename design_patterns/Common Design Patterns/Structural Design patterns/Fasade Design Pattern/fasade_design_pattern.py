"""Fasade """

import os


# 1️⃣ Complex System
class VideoFile:
    """Represents a video file."""

    def __init__(self, filename):
        self.filename = filename

    def get_info(self):
        return f"VideoFile: {self.filename}"


class Codec:
    """Base class for different video codecs."""

    pass


class H264Codec(Codec):
    """H.264 codec for video compression."""

    def compress(self, filename):
        print(f"Compressing {filename} using H.264 codec...")


class MPEG4Codec(Codec):
    """MPEG4 codec for video compression."""

    def compress(self, filename):
        print(f"Compressing {filename} using MPEG4 codec...")


class AudioMixer:
    """Handles audio processing."""

    def mix_audio(self, filename):
        print(f"Mixing audio for {filename}...")


class VideoConverter:
    """Handles video format conversion using ffmpeg."""

    def convert(self, filename, format):
        print(f"Converting {filename} to {format} format...")
        os.system(f"ffmpeg -i {filename} output.{format}")


class Watermark:
    """Applies watermark to the video."""

    def apply(self, filename, watermark):
        print(f"Applying watermark '{watermark}' to {filename}...")


# 2️⃣ Simple Facade interface
class VideoProcessingFacade:
    """Facade that simplifies video processing tasks."""

    def __init__(self):
        self.audio_mixer = AudioMixer()
        self.video_converter = VideoConverter()
        self.watermark_processor = Watermark()

    def process_video(self, filename, output_format, codec="h264", watermark_text=None):
        print("\n--- Video Processing Started ---")

        # Select codec
        codec_processor = H264Codec() if codec == "h264" else MPEG4Codec()

        # Mix audio
        self.audio_mixer.mix_audio(filename)

        # Convert video
        self.video_converter.convert(filename, output_format)

        # Compress video
        codec_processor.compress(filename)

        # Apply watermark if needed
        if watermark_text:
            self.watermark_processor.apply(filename, watermark_text)

        print("--- Video Processing Completed ---\n")


if __name__ == "__main__":
    facade = VideoProcessingFacade()

    # Process a video (convert to mp4, use h264 codec, apply watermark)
    facade.process_video(
        "sample_video.avi", "mp4", codec="h264", watermark_text="My Watermark"
    )
