"""
AI Analysis Router (boilerplate — not runnable as-is)
"""

from fastapi import APIRouter, Depends, UploadFile, Form

from strategy_ai_analysis_service import AIAnalysisService, ImageUploader

router = APIRouter(prefix="/ai-analysis", tags=["AI Analysis"])


# ── Dependency injection ──────────────────────────────────────────────────────

def get_service() -> AIAnalysisService:
    return AIAnalysisService(uploader=ImageUploader())


# ── Routes ────────────────────────────────────────────────────────────────────

@router.post("/odometer")
async def analyze_odometer(
    image: UploadFile,
    extra_data: str = Form(...),
    service: AIAnalysisService = Depends(get_service),
):
    return await service.process("odometer", image.filename, {"raw": extra_data})


@router.post("/chasis")
async def analyze_chasis(
    image: UploadFile,
    extra_data: str = Form(...),
    service: AIAnalysisService = Depends(get_service),
):
    return await service.process("chasis", image.filename, {"raw": extra_data})
