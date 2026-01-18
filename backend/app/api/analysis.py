from fastapi import APIRouter
from app.schemas.analysis import JobAnalysisRequest, JobAnalysisResponse, ScoreBreakdown

router = APIRouter()


@router.post("/analyze", response_model=JobAnalysisResponse)
async def analyze_job(request: JobAnalysisRequest):
    """Analyze visa sponsorship likelihood for a job posting"""
    return JobAnalysisResponse(
        visa_likelihood_score=0.65,
        score_breakdown=ScoreBreakdown(
            jd_language_score=0.7,
            role_feasibility_score=0.6,
            company_history_score=0.5,
            heuristic_score=0.8
        ),
        explanation="Placeholder - real intelligence engine coming in next step",
        country_code="US",
        confidence_level="medium"
    )
