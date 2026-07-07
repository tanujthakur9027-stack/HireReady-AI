import json
from pydantic import BaseModel, Field
from services.gemini_service import get_client

class JDMatcherSchema(BaseModel):
    score: int = Field(..., description="Semantic match score out of 100 between resume and job description")
    matched: list[str] = Field(..., description="Skills required in the JD that are found in the resume")
    missing: list[str] = Field(..., description="Crucial skills required in the JD that are missing in the resume")
    alignment_summary: str = Field(..., description="Detailed explanation of how well the candidate aligns with the role")
    strengths_for_role: list[str] = Field(..., description="Top candidate strengths that map directly to the JD")
    gaps_for_role: list[str] = Field(..., description="Gaps in candidate's experience or skills for this specific JD")

PROMPT = """
You are an expert Talent Acquisition Consultant.
Analyze the candidate's resume text against the provided Job Description (JD).
1. Compare the core tech stack, experience, and responsibilities.
2. Determine the semantic match score (0 to 100) based on alignment.
3. Identify which skills required in the JD are present (matched) and which are missing (missing).
4. Summarize how well the candidate aligns with the role, highlighting direct strengths and key gaps.
"""

def match_resume(resume, jd):
    client = get_client()
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"{PROMPT}\n\nResume:\n{resume}\n\nJob Description:\n{jd}",
            config={
                "response_mime_type": "application/json",
                "response_schema": JDMatcherSchema
            }
        )
        return json.loads(response.text)
    except Exception as e:
        # Fallback in case of API issues
        return {
            "score": 50,
            "matched": [],
            "missing": ["Could not parse due to API error"],
            "alignment_summary": f"An error occurred during JD matching: {str(e)}",
            "strengths_for_role": [],
            "gaps_for_role": ["Failed to extract gaps"]
        }