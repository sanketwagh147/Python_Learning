"""
AI Analysis Service (Strategy Pattern)

SOLID compliance:
- SRP : ImageUploader uploads, each Strategy analyses, Service orchestrates
- OCP : Add new analysis types by adding a Strategy + map entry — zero changes to existing code
- LSP : All strategies are interchangeable via AIAnalysisStrategy
- ISP : Strategy interface exposes only what analysis needs
- DIP : Service depends on abstractions (AIAnalysisStrategy, ImageUploader), not concretions
"""

from abc import ABC, abstractmethod


# ── Abstraction (ISP: only analysis-relevant methods) ────────────────────────

class AIAnalysisStrategy(ABC):
    @abstractmethod
    async def analyse(self, s3_url: str, meta: dict) -> dict:
        pass

    @abstractmethod
    async def formulate_response(self, ai_result: dict) -> dict:
        pass


# ── Concrete strategies (SRP: one responsibility each) ───────────────────────

class OdometerStrategy(AIAnalysisStrategy):
    async def analyse(self, s3_url: str, meta: dict) -> dict:
        # call odometer AI model here
        return {"odometer_reading": 45231}

    async def formulate_response(self, ai_result: dict) -> dict:
        return {"odometer_reading": ai_result["odometer_reading"]}


class ChasisStrategy(AIAnalysisStrategy):
    async def analyse(self, s3_url: str, meta: dict) -> dict:
        # call chassis AI model here
        return {"chassis_number": "ABC123XYZ456"}

    async def formulate_response(self, ai_result: dict) -> dict:
        return {"chassis_number": ai_result["chassis_number"]}


# ── Single-purpose uploader (SRP) ────────────────────────────────────────────

class ImageUploader:
    async def upload(self, meta: dict) -> str:
        # upload to S3 / DMS here
        return f"https://s3.amazonaws.com/bucket/{meta['filename']}"


# ── Strategy map (OCP: extend by adding entries, never by modifying) ─────────

STRATEGY_MAP: dict[str, AIAnalysisStrategy] = {
    "odometer": OdometerStrategy(),
    "chasis": ChasisStrategy(),
}


# ── Service (DIP: depends on abstractions, injected at construction) ─────────

class AIAnalysisService:
    def __init__(
        self,
        uploader: ImageUploader,
        strategies: dict[str, AIAnalysisStrategy] = STRATEGY_MAP,
    ):
        self._uploader = uploader
        self._strategies = strategies

    async def process(self, analysis_type: str, filename: str, extra_data: dict) -> dict:
        strategy = self._strategies.get(analysis_type)
        if not strategy:
            raise ValueError(f"Unsupported analysis type: '{analysis_type}'")

        meta = {"filename": filename, "extra": extra_data}
        s3_url = await self._uploader.upload(meta)
        ai_result = await strategy.analyse(s3_url, meta)
        return await strategy.formulate_response(ai_result)
