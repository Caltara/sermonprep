import json
from openai import OpenAI
import streamlit as st

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def generate_sermon_series(theme: str, weeks: int):
    prompt = f"""
You are a helpful assistant that creates sermon series for pastors.

Create a {weeks}-week sermon series about "{theme}".

For each week, provide:
- A sermon title
- A 2-3 sentence summary
- 3-5 NKJV Bible verses

Format the response as a valid JSON list, like this:

[
  {{
    "week": 1,
    "title": "Title here",
    "summary": "Summary here.",
    "verses": ["John 3:16", "Romans 8:28"]
  }},
  ...
]
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1800,
        temperature=0.7,
    )

    content = response.choices[0].message.content.strip()

    # Attempt to extract JSON block if OpenAI response includes extra text
    try:
        json_start = content.find("[")
        json_end = content.rfind("]") + 1
        json_text = content[json_start:json_end]
        parsed = json.loads(json_text)
        return parsed
    except Exception:
        # Fallback: return the entire message as a single item
        return [{
            "week": 1,
            "title": theme,
            "summary": content,
            "verses": []
        }]
