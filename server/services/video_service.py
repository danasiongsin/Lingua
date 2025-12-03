import os
import tempfile
from pathlib import Path
from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech
from moviepy import VideoFileClip
from dotenv import load_dotenv

load_dotenv()

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
    Transcribe audio file using Google Speech-to-Text v2 API.

    Args:
        audio_path: Path to the audio file

    Returns:
        Transcribed text
    """
    try:
        # Verify credentials are set
        credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        if not credentials_path:
            raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set")

        if not os.path.exists(credentials_path):
            raise ValueError(f"Credentials file not found at: {credentials_path}")

        print(f"Using credentials from: {credentials_path}")

        # Initialize the Speech-to-Text v2 client
        client = SpeechClient()

        # Read the audio file
        with open(audio_path, "rb") as audio_file:
            content = audio_file.read()

        # Configure recognition settings for v2 API with Spanish and English support
        config = cloud_speech.RecognitionConfig(
            auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
            language_codes=["es-ES", "en-US"],  # Support both Spanish and English
            model="long",
            features=cloud_speech.RecognitionFeatures(
                enable_automatic_punctuation=True,
            ),
        )

        # Build the request - use project ID from credentials
        # First try environment variable, then extract from credentials file
        project_id = os.getenv('GOOGLE_CLOUD_PROJECT')

        if not project_id:
            # Extract project_id from credentials file
            import json
            with open(credentials_path, 'r') as f:
                creds_data = json.load(f)
                project_id = creds_data.get('project_id', 'gen-lang-client-0982694589')

        print(f"Using project ID: {project_id}")

        request = cloud_speech.RecognizeRequest(
            recognizer=f"projects/{project_id}/locations/global/recognizers/_",
            config=config,
            content=content,
        )

        print("Starting transcription with Speech-to-Text v2...")

        # Perform the transcription
        response = client.recognize(request=request)

        print("Transcription completed.")

        # Combine all transcription results
        transcript = ""
        for result in response.results:
            transcript += result.alternatives[0].transcript + " "

        return transcript.strip()

    except Exception as e:
        print(f"Error during transcription: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        raise Exception(f"Transcription failed: {str(e)}")


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

        print("Audio extracted to:", audio_path)

        # Transcribe the audio
        transcript = await transcribe_audio(audio_path)

        return transcript
    finally:
        # Clean up temporary audio file
        if audio_path and os.path.exists(audio_path):
            os.remove(audio_path)
