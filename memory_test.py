from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env", override=True)

print("Current Folder:", os.getcwd())
print("Env Exists:", os.path.exists(".env"))
print("LLM_API_KEY:", os.getenv("LLM_API_KEY"))
print("LLM_PROVIDER:", os.getenv("LLM_PROVIDER"))
print("LLM_MODEL:", os.getenv("LLM_MODEL"))

import cognee
import asyncio
import cognee


async def test():
    print("Saving memory...")

    await cognee.remember(
        """
        User name is Tanuj.
        Preparing for AI/ML Engineer interviews.
        Weak topic: SQL joins.
        Strong topic: Python.
        """
    )

    print("Memory saved.")

    print("\nSearching memory...\n")

    result = await cognee.recall(
        "What are the user's weak topics?"
    )

    print(result)


asyncio.run(test())
