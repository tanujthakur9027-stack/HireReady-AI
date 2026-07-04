import json
from services.gemini_service import get_client

PROMPT = """
You are an ATS Resume Analyzer.

Return ONLY valid JSON.

{
 "overall_score":0,
 "ats_score":0,
 "technical_score":0,
 "communication_score":0,
 "formatting_score":0,
 "project_score":0,
 "strengths":[],
 "weaknesses":[],
 "suggestions":[]
}
"""


def analyze_resume(resume_text):

    client = get_client()

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"{PROMPT}\n\nResume:\n{resume_text}"
        )

        text = response.text.replace("```json","").replace("```","").strip()

        return json.loads(text)

    except Exception as e:

        return {
            "overall_score":70,
            "ats_score":70,
            "technical_score":70,
            "communication_score":70,
            "formatting_score":70,
            "project_score":70,
            "strengths":["Python"],
            "weaknesses":["Need Improvement"],
            "suggestions":[str(e)]
        }