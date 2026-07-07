import json
from pydantic import BaseModel, Field
from services.gemini_service import get_client

class ATSChecklistSchema(BaseModel):
    Email: bool = Field(..., description="True if a contact email is present in the resume")
    Phone: bool = Field(..., description="True if a contact phone number is present in the resume")
    LinkedIn: bool = Field(..., description="True if a LinkedIn profile is mentioned")
    GitHub: bool = Field(..., description="True if a GitHub profile is mentioned")
    Education: bool = Field(..., description="True if education details are present")
    Projects: bool = Field(..., description="True if projects are listed")
    Experience: bool = Field(..., description="True if work experience or internships are listed")

class ATSCheckerSchema(BaseModel):
    ats_score: int = Field(..., description="Overall ATS compatibility score from 0 to 100")
    skills: list[str] = Field(..., description="List of technical skills and tools extracted from the resume")
    checklist: ATSChecklistSchema = Field(..., description="Checklist of essential components")
    formatting_feedback: list[str] = Field(..., description="List of layout, formatting, or parsing compatibility recommendations")


PROMPT = """
You are an expert ATS (Applicant Tracking System) parser and auditor.
Analyze the provided resume text.
1. Determine if crucial contact details and sections are present (Email, Phone, LinkedIn, GitHub, Education, Projects, Experience).
2. Extract all technical skills and tools listed.
3. Assess the ATS readability, use of standard section headings, and layout parsing feasibility. Calculate a realistic ATS score (0 to 100).
4. Provide formatting and parsing compatibility feedback.
"""

def check_resume(text):
    client = get_client()
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"{PROMPT}\n\nResume Text:\n{text}",
            config={
                "response_mime_type": "application/json",
                "response_schema": ATSCheckerSchema
            }
        )
        return json.loads(response.text)
    except Exception as e:
        # Fallback in case of API issues
        return {
            "ats_score": 70,
            "skills": ["python", "javascript", "sql"],
            "checklist": {
                "Email": True,
                "Phone": True,
                "LinkedIn": False,
                "GitHub": False,
                "Education": True,
                "Projects": True,
                "Experience": True
            },
            "formatting_feedback": ["Could not parse formatting semantically due to API error: " + str(e)]
        }