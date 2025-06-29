from openai import OpenAI
import streamlit as st

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def generate_sermon_series(theme: str, weeks: int):
    prompt = f"""
You are a helpful assistant that creates sermon series plans.

Create a {weeks}-week sermon series about "{theme}".
For each week, provide:
- A sermon title
- A brief summary (1-2 sentences)
- Suggested NKJV Bible verses (3-5 verses)

Format your response as a numbered list, with each week clearly labeled.
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=800,
        temperature=0.7,
    )

    text = response.choices[0].message.content

    # Basic parsing: split by lines and group by weeks
    series = []
    current_week = {}
    lines = text.splitlines()
    for line in lines:
        line = line.strip()
        if line.lower().startswith("week"):
            if current_week:
                series.append(current_week)
            current_week = {"title": "", "summary": "", "verses": []}
        elif line.lower().startswith("- a sermon title"):
            current_week["title"] = line.split(":", 1)[-1].strip()
        elif line.lower().startswith("- a brief summary"):
            current_week["summary"] = line.split(":", 1)[-1].strip()
        elif line.lower().startswith("- suggested"):
            verses_part = line.split(":", 1)[-1].strip()
            verses = [v.strip() for v in verses_part.split(",")]
            current_week["verses"] = verses
        else:
            # Attempt to extract titles, summaries, verses from formatted lines
            # For simplicity, assume lines like "1. Title: xyz", "Summary: abc", "Verses: ..."
            if line.startswith(tuple(str(i) + "." for i in range(1, weeks + 1))):
                if current_week:
                    series.append(current_week)
                current_week = {"title": "", "summary": "", "verses": []}
                # parse title from this line
                if ":" in line:
                    current_week["title"] = line.split(":",1)[1].strip()
            elif line.lower().startswith("summary:"):
                current_week["summary"] = line.split(":",1)[1].strip()
            elif line.lower().startswith("bible verses:"):
                verses = line.split(":",1)[1].strip().split(",")
                current_week["verses"] = [v.strip() for v in verses]
    if current_week:
        series.append(current_week)

    # Fallback: if parsing fails, just return raw text as one item
    if not series:
        return [{"title": theme, "summary": text, "verses": []}]

    return series
