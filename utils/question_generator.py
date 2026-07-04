from services.gemini_service import get_client

client = get_client()


def generate_question(role, company, difficulty):

    prompt = f"""
You are a FAANG coding interviewer.

Generate ONE coding interview question.

Role:
{role}

Company:
{company}

Difficulty:
{difficulty}

Return ONLY in this format:

TITLE:
DESCRIPTION:
INPUT:
OUTPUT:
CONSTRAINTS:
EXAMPLE:
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text