"""
generate_quote.py — ask Gemini (free tier) for an original line + caption + hashtags.
Returns a dict: {"quote": str, "caption": str, "hashtags": [str, ...]}
"""
import os
import json
from google import genai
from google.genai import types
import config

PROMPT = f"""{config.VOICE_BRIEF}

Produce ONE social post. Return STRICT JSON only, no markdown, no backticks, with keys:
- "quote": one original line, max 16 words, the text that goes ON the image.
- "caption": 1-2 short sentences expanding the idea, written to the same voice. No hashtags here.
- "hashtags": an array of 10 lowercase hashtags (no '#'), mixing discipline / fitness /
  self-improvement / mindset niches, a couple smaller-reach ones for discoverability.

Make it land. Avoid cliches like "no pain no gain". Keep it sharp and quiet.
"""


def generate() -> dict:
    api_key = os.environ["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
    resp = client.models.generate_content(
        model=config.GEMINI_MODEL,
        contents=PROMPT,
        config=types.GenerateContentConfig(
            temperature=1.0,
            response_mime_type="application/json",
        ),
    )
    data = json.loads(resp.text)
    # normalise hashtags -> "#tag" string for the caption
    tags = data.get("hashtags", [])
    data["hashtag_line"] = " ".join("#" + t.lstrip("#") for t in tags)
    return data


if __name__ == "__main__":
    print(json.dumps(generate(), indent=2, ensure_ascii=False))
