import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM = (
    "You are a pastor creating teaching outlines for church lessons. "
    "Use bullet points with short descriptions. Include suggested Bible references "
    "without quoting the text. End with a takeaway or challenge."
)

def generate_teaching_outline(subject: str, idea: str) -> str:
    prompt = (
        f"Subject: {subject}\n"
        f"Concept: {idea}\n\n"
        "Create a 3-point teaching outline with sub-points and suggested Bible references."
    )
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": prompt}
        ],
        temperature=0.6,
        max_tokens=1000
    )
    return response.choices[0].message.content.strip()
