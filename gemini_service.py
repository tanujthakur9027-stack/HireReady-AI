import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """
You are InterviewMate AI.

You are an expert technical interviewer.

Rules:
- Conduct a professional interview.
- Ask only ONE question at a time.
- Wait for the candidate's answer.
- Ask follow-up questions based on previous answers.
- If a resume is provided, ask questions from the resume.
- Adjust difficulty according to the candidate's performance.
- Never answer your own interview questions.
- At the end of the interview, provide:
  1. Overall Score (/100)
  2. Technical Skills Score
  3. Communication Score
  4. Strengths
  5. Weaknesses
  6. Learning Recommendations
"""

chat = client.chats.create(
    model="gemini-2.5-flash",
    config={
        "system_instruction": SYSTEM_PROMPT
    }
)


def ask_ai(message, profile):

    prompt = f"""
Candidate Name:
{profile['name']}

Target Role:
{profile['role']}

Target Company:
{profile['company']}

Resume:
{profile['resume']}

Candidate Response:
{message}

Continue the interview.

Rules:
- Ask only ONE interview question.
- Use the resume if available.
- Increase or decrease difficulty based on the candidate's previous answer.
- Do not provide the final evaluation until the interview is complete.
"""

    response = chat.send_message(prompt)

    return response.text