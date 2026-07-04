from google import genai
from services.gemini_service import get_client

client = get_client()


def review_code(question, code):

    prompt = f"""
You are a Senior FAANG Coding Interviewer.

Question:

{question}

Candidate Code:

{code}

Evaluate the code and return the following in Markdown format:

# Overall Score (/100)

# Correctness

# Time Complexity

# Space Complexity

# Strengths

# Mistakes

# Optimized Solution

# Interview Feedback

Be concise but detailed.
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:

        return f"❌ Error: {e}"