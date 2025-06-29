import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM = (
    "You are a pastor creating biblically faithful sermons. "
    "Do not quote Bible passages. Instead, suggest relevant Bible references (e.g. John 3:16). "
    "Include an intro, 2-3 main points, and a conclusion."
)

def generate_sermon(title: str, summary: str) -> str:
    prompt = (
        f"Title: {title}\n"
        f"Summary: {summary}\n\n"
        "Write a sermon with introduction, 2-3 main points, and a closing application. "
        "Only suggest Bible references, do not quote text."
    )
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1200
    )
    return response.choices[0].message.content.strip()
