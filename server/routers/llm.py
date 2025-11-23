from fastapi import APIRouter, HTTPException
from server.services.llm_service import call_llm

router = APIRouter()

@router.post("/generate")
async def generate_text(prompt: str):
    try:
        result = await call_llm(prompt)
        return {"output": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
