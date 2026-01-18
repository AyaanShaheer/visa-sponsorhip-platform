from pydantic import BaseModel
from typing import Dict, List


class JobAnalysisRequest(BaseModel):
    job_title: str
    company_name: str
    location: str
    job_description: str
    job_url: str


class ScoreBreakdown(BaseModel):
    jd_language_score: float
    role_feasibility_score: float
    company_history_score: float
    heuristic_score: float


class JobAnalysisResponse(BaseModel):
    visa_likelihood_score: float
    score_breakdown: ScoreBreakdown
    explanation: str
    country_code: str
    confidence_level: str
