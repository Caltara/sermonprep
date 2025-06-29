import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM = (
    "You are a Bible teacher creating a group Bible study guide. "
    "Include an introduction, 2-3 main questions with relevant verse references, "
    "and 1-2 reflection or application questions. Do not quote scripture."
)

def generate_bible_study(topic: str, notes: str) -> str:
    prompt = (
        f"Topic: {topic}\n"
        f"Summary: {notes}\n\n"
        "Create a Bible study guide. Include intro, questions, and verse references."
    )
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1000
    )
    return response.choices[0].message.content.strip()
