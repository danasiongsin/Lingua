import os
import tempfile
from fastapi import APIRouter, HTTPException, UploadFile, File
from services.llm_service import call_llm
from services.video_service import process_video

router = APIRouter()

@router.post("/process-video")
async def process_video_endpoint(video: UploadFile = File(...)):
    """
    Accept a video file, extract audio, transcribe it using Google Speech-to-Text,
    and feed the transcribed text through the AI Agent.

    Args:
        video: MP4 video file

    Returns:
        Object containing transcription and AI agent response
    """
    video_path = None
    try:
        # Validate filename extension
        if not video.filename or not video.filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.webm')):
            raise HTTPException(
                status_code=400,
                detail="Invalid file type. Please upload a video file (mp4, avi, mov, mkv, webm)."
            )

        # Save uploaded video to temporary file
        video_fd, video_path = tempfile.mkstemp(suffix=".mp4")
        os.close(video_fd)

        with open(video_path, "wb") as f:
            content = await video.read()
            f.write(content)

        # Process video: extract audio and transcribe
        transcript = await process_video(video_path)

        if not transcript:
            raise HTTPException(
                status_code=400,
                detail="No speech detected in the video"
            )

        # Feed transcription through AI agent
        ai_response = await call_llm(transcript)

        return {
            "transcript": transcript,
            "ai_response": ai_response
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing video: {str(e)}")
    finally:
        # Clean up temporary video file
        if video_path and os.path.exists(video_path):
            os.remove(video_path)
