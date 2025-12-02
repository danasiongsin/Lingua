import os
import tempfile
from pathlib import Path
from google.cloud import speech
from moviepy import VideoFileClip
from config import settings

async def extract_audio_from_video(video_path: str) -> str:
    """
    Extract audio from video file and save as WAV format.

    Args:
        video_path: Path to the video file

    Returns:
        Path to the extracted audio file
    """
    video = VideoFileClip(video_path)

    # Create temporary file for audio
    audio_fd, audio_path = tempfile.mkstemp(suffix=".wav")
    os.close(audio_fd)

    # Extract audio and save as WAV
    video.audio.write_audiofile(audio_path, codec='pcm_s16le')
    video.close()

    return audio_path


async def transcribe_audio(audio_path: str) -> str:
    """
    Transcribe audio file using Google Speech-to-Text API.

    Args:
        audio_path: Path to the audio file

    Returns:
        Transcribed text
    """
    # Initialize the Speech-to-Text client
    client = speech.SpeechClient()

    # Read the audio file
    with open(audio_path, "rb") as audio_file:
        content = audio_file.read()

    # Configure recognition settings
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code="en-US",
        enable_automatic_punctuation=True,
    )

    # Perform the transcription
    response = client.recognize(config=config, audio=audio)

    # Combine all transcription results
    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript + " "

    return transcript.strip()


async def process_video(video_path: str) -> str:
    """
    Process video file: extract audio, transcribe, and clean up temporary files.

    Args:
        video_path: Path to the video file

    Returns:
        Transcribed text from the video
    """
    audio_path = None
    try:
        # Extract audio from video
        audio_path = await extract_audio_from_video(video_path)

        # Transcribe the audio
        transcript = await transcribe_audio(audio_path)

        return transcript
    finally:
        # Clean up temporary audio file
        if audio_path and os.path.exists(audio_path):
            os.remove(audio_path)
