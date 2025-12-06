import os
import tempfile
from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from services.video_service import process_video
from services.agent_service import agent_service

router = APIRouter()


class GenerateExamplesRequest(BaseModel):
    item_type: str  # 'vocab' or 'grammar'
    word: str = None
    translation: str = None
    structure_name: str = None

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


@router.post("/generate-examples")
async def generate_examples(request: GenerateExamplesRequest):
    """
    Generate detailed information and additional examples for vocabulary or grammar items.

    Args:
        request: Contains item_type ('vocab' or 'grammar') and relevant fields

    Returns:
        Object containing detailed description and example sentences
    """
    try:
        if request.item_type not in ['vocab', 'grammar']:
            raise HTTPException(
                status_code=400,
                detail="item_type must be either 'vocab' or 'grammar'"
            )

        if request.item_type == 'vocab' and (not request.word or not request.translation):
            raise HTTPException(
                status_code=400,
                detail="word and translation are required for vocab items"
            )

        if request.item_type == 'grammar' and not request.structure_name:
            raise HTTPException(
                status_code=400,
                detail="structure_name is required for grammar items"
            )

        result = await agent_service.generate_detailed_info(
            item_type=request.item_type,
            word=request.word or request.structure_name,
            translation=request.translation,
            structure_name=request.structure_name
        )

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating examples: {str(e)}")
