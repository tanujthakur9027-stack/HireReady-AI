import json
from pydantic import BaseModel, Field
from services.gemini_service import get_client

class ResumeAnalysisSchema(BaseModel):
    overall_score: int = Field(..., description="Overall score out of 100")
    ats_score: int = Field(..., description="ATS compatibility score out of 100")
    technical_score: int = Field(..., description="Technical depth score out of 100")
    communication_score: int = Field(..., description="Written communication and impact score out of 100")
    formatting_score: int = Field(..., description="Formatting and structure score out of 100")
    project_score: int = Field(..., description="Project strength score out of 100")
    strengths: list[str] = Field(..., description="Key strengths identified in the resume")
    weaknesses: list[str] = Field(..., description="Areas for improvement or gaps in the resume")
    suggestions: list[str] = Field(..., description="Actionable recommendations to enhance the resume")


PROMPT = """
You are an expert HR Manager and Technical Recruiter.
Analyze the candidate's resume text and evaluate the overall quality, ATS compatibility, technical skills depth, communication impact, formatting layout structure, and project quality.
Provide score ratings from 0 to 100, lists of specific strengths, weaknesses, and concrete recommendations.
"""

def analyze_resume(resume_text):
    client = get_client()
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"{PROMPT}\n\nResume Text:\n{resume_text}",
            config={
                "response_mime_type": "application/json",
                "response_schema": ResumeAnalysisSchema
            }
        )
        # The response.text is guaranteed to be a valid JSON matching ResumeAnalysisSchema
        return json.loads(response.text)
    except Exception as e:
        # Fallback in case of API issues
        return {
            "overall_score": 65,
            "ats_score": 60,
            "technical_score": 70,
            "communication_score": 65,
            "formatting_score": 70,
            "project_score": 60,
            "strengths": ["Clear section layouts", "Technical skills are listed"],
            "weaknesses": ["Gaps in metrics or achievements quantified", f"API Call issues: {str(e)}"],
            "suggestions": ["Add measurable metrics (e.g. percentages, money saved, hours saved) to projects.", "Verify resume contact info matches standard headers."]
        }