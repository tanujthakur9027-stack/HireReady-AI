import json
from pydantic import BaseModel, Field
from services.gemini_service import get_client

class QAReviewSchema(BaseModel):
    question: str = Field(..., description="The question asked by the interviewer")
    answer: str = Field(..., description="The answer given by the candidate")
    score: int = Field(..., description="Score rating from 0 to 100 for this answer")
    strengths: str = Field(..., description="Key strengths of the answer")
    gaps: str = Field(..., description="Gaps, inefficiencies, or missing points in the answer")
    ideal_answer: str = Field(..., description="An example of an ideal answer for this question")

class InterviewEvaluationSchema(BaseModel):
    overall_feedback: str = Field(..., description="High-level feedback summarizing the overall interview performance")
    technical_score: int = Field(..., description="Technical rating out of 100")
    communication_score: int = Field(..., description="Communication rating out of 100")
    confidence_score: int = Field(..., description="Confidence and professional presence rating out of 100")
    strong_topics: list[str] = Field(..., description="Topics the candidate excelled in")
    weak_topics: list[str] = Field(..., description="Topics where the candidate struggled")
    mistakes: list[str] = Field(..., description="Specific errors, misconceptions, or bugs made in the interview")
    recommended_topics: list[str] = Field(..., description="Topics recommended for study and review")
    qa_review: list[QAReviewSchema] = Field(..., description="Question-by-question analysis breakdown")

PROMPT = """
You are a Lead FAANG Technical Recruiter.
Analyze the complete transcript of the mock interview.
Assess the technical content, communication effectiveness, and overall confidence.
Provide:
1. High-level summary of their performance (overall_feedback).
2. Scores for technical, communication, and confidence.
3. Identified strong and weak topics.
4. Specific mistakes or misconceptions.
5. Study recommendations.
6. A detailed breakdown of each Question and the candidate's corresponding Answer, highlighting strengths, gaps, and providing an ideal model answer.
"""

def build_memory(messages):
    client = get_client()
    conversation = ""
    for msg in messages:
        role_name = "Interviewer" if msg['role'] == "assistant" else "Candidate"
        conversation += f"{role_name}: {msg['content']}\n\n"

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"{PROMPT}\n\nInterview Transcript:\n{conversation}",
            config={
                "response_mime_type": "application/json",
                "response_schema": InterviewEvaluationSchema
            }
        )
        return json.loads(response.text)
    except Exception as e:
        # Fallback evaluation
        return {
            "overall_feedback": f"Could not perform structured evaluation due to API error: {str(e)}",
            "technical_score": 75,
            "communication_score": 75,
            "confidence_score": 75,
            "strong_topics": ["General concepts"],
            "weak_topics": ["Error logs"],
            "mistakes": ["System error occurred during compilation"],
            "recommended_topics": ["Review transcript manually"],
            "qa_review": []
        }