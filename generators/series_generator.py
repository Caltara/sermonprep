import json
from openai import OpenAI
import streamlit as st

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def generate_sermon_series(theme: str, weeks: int):
    prompt = f"""
Create a {weeks}-week sermon series about "{theme}".

For each week, provide:
- A sermon title
- A 2-3 sentence summary of the sermon message
- 3-5 suggested NKJV Bible verses, listed clearly

Please format your response as valid JSON as a list of objects with keys: week, title, summary, verses.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000,
        temperature=0.7,
    )

    text = response.choices[0].message.content

    try:
        series = json.loads(text)
    except json.JSONDecodeError:
        # Fallback: return raw text as one item if parsing fails
        series = [{"week": 1, "title": theme, "summary": text, "verses": []}]

    return series
