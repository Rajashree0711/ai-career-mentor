import json
from google import genai
from config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

def analyze_resume(resume_text: str) -> dict:
    prompt = f"""
You are an expert ATS (Applicant Tracking System) and career coach.

Analyze the following resume text and respond with ONLY a valid JSON object,
no other text, no markdown formatting, no code blocks.

The JSON must have exactly this structure:
{{
  "ats_score": <integer between 0 and 100>,
  "strengths": ["strength 1", "strength 2", "strength 3"],
  "weaknesses": ["weakness 1", "weakness 2", "weakness 3"],
  "missing_skills": ["skill 1", "skill 2", "skill 3"]
}}

Resume text:
{resume_text}
"""

    response = client.models.generate_content(
    model="gemini-flash-latest",
    contents=prompt
)

    raw_output = response.text.strip()

    if raw_output.startswith("```"):
        raw_output = raw_output.strip("`")
        if raw_output.startswith("json"):
            raw_output = raw_output[4:]

    result = json.loads(raw_output)
    return result