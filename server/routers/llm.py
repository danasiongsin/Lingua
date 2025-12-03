import os
import tempfile
from fastapi import APIRouter, HTTPException, UploadFile, File
from services.video_service import process_video
from services.agent_service import agent_service

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

        print("Video saved to:", video_path)

        # Process video: extract audio and transcribe
        transcript = await process_video(video_path)

        print("Transcription:", transcript)

        if not transcript:
            raise HTTPException(
                status_code=400,
                detail="No speech detected in the video"
            )

        # Feed transcription through AI agent to generate lesson plan
        lesson_plan = await agent_service.generate_lesson_plan(transcript)

        print("Lesson Plan generated.", lesson_plan)

        return {
            "transcript": transcript,
            "lesson_plan": lesson_plan
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing video: {str(e)}")
    finally:
        # Clean up temporary video file
        if video_path and os.path.exists(video_path):
            os.remove(video_path)
