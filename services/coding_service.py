import json
from pydantic import BaseModel, Field
from services.gemini_service import get_client

class CodingReviewSchema(BaseModel):
    score: int = Field(..., description="Overall code evaluation score out of 100")
    correctness: str = Field(..., description="Detailed correctness analysis, edge cases tested, and bugs found")
    time_complexity: str = Field(..., description="Time complexity analysis (e.g. O(N)) with explanation")
    space_complexity: str = Field(..., description="Space complexity analysis (e.g. O(1)) with explanation")
    strengths: list[str] = Field(..., description="Key strengths of the implementation")
    mistakes: list[str] = Field(..., description="Bugs, inefficiencies, edge case failures, or code style issues")
    optimized_solution: str = Field(..., description="Full optimized Python code implementation")
    feedback: str = Field(..., description="Constructive advice and general feedback for the candidate")

def review_code(question, code):
    client = get_client()
    prompt = f"""
You are a Senior FAANG Coding Interviewer.
Evaluate the candidate's implementation of the following question.

Coding Question:
{question}

Candidate Code:
{code}
"""
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": CodingReviewSchema
            }
        )
        return json.loads(response.text)
    except Exception as e:
        return {
            "score": 50,
            "correctness": f"Error running review: {str(e)}",
            "time_complexity": "N/A",
            "space_complexity": "N/A",
            "strengths": ["Code was submitted"],
            "mistakes": ["Failed to analyze due to API issue"],
            "optimized_solution": "# No optimized solution available",
            "feedback": "Please try submitting again."
        }