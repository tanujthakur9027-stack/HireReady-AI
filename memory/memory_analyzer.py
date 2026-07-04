import json
from google import genai
from services.gemini_service import get_client

client = get_client()

PROMPT = """
You are an AI Memory Builder.

Analyze the interview conversation.

Return ONLY valid JSON.

{
    "technical_score": 82,
    "communication_score": 74,
    "confidence_score": 80,

    "strong_topics": [],

    "weak_topics": [],

    "mistakes": [],

    "recommended_topics": []
}
"""


def build_memory(messages):

    conversation = ""

    for msg in messages:

        conversation += f"{msg['role']}: {msg['content']}\n"

    try:

        response = client.models.generate_content(

            model="gemini-2.5-flash",

            contents=PROMPT + "\n\n" + conversation

        )

        text = response.text.strip()

        text = text.replace("```json", "")
        text = text.replace("```", "")

        return json.loads(text)

    except:

     return {

    "technical_score":80,

    "communication_score":75,

    "confidence_score":82,

    "strong_topics":["Python"],

    "weak_topics":["SQL"],

    "mistakes":[],

    "recommended_topics":["DBMS"]
}  