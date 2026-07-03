import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

# Load .env for local development
load_dotenv()

# Read API Key
api_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY not found. Add it to .env (local) or Streamlit Secrets."
    )

# Gemini Client
client = genai.Client(api_key=api_key)

SYSTEM_PROMPT = """
You are InterviewMate AI.

You are a Senior Technical Interviewer.

Your job is to conduct a realistic mock interview.

Rules:

- Ask ONLY one question at a time.
- Wait for the candidate's answer.
- Ask follow-up questions based on previous responses.
- If resume is available, ask resume-based questions.
- Increase or decrease difficulty according to performance.
- Never answer your own interview questions.

When the interview ends provide:

1. Overall Score (/100)
2. Technical Score
3. Communication Score
4. Strengths
5. Weaknesses
6. Improvement Plan
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

- Ask ONLY one interview question.
- Use resume if available.
- Ask follow-up questions.
- Do NOT provide final evaluation until the interview ends.
"""

    try:
        response = chat.send_message(prompt)
        return response.text

    except Exception as e:
        return f"❌ Gemini Error: {str(e)}"