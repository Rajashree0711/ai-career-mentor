import json
from google import genai
from config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

def generate_roadmap(resume_text: str, missing_skills: list, weaknesses: list) -> dict:
    prompt = f"""
You are an expert career coach and technical interviewer.

Based on the resume text, missing skills, and weaknesses below, create:
1. A 4-week, week-by-week learning plan to close the missing skills
2. 5 relevant interview questions this candidate should prepare for, with a short model answer for each

Respond with ONLY a valid JSON object, no other text, no markdown formatting, no code blocks.

The JSON must have exactly this structure:
{{
  "learning_plan": [
    {{"week": 1, "focus": "short title", "tasks": ["task 1", "task 2"]}},
    {{"week": 2, "focus": "short title", "tasks": ["task 1", "task 2"]}},
    {{"week": 3, "focus": "short title", "tasks": ["task 1", "task 2"]}},
    {{"week": 4, "focus": "short title", "tasks": ["task 1", "task 2"]}}
  ],
  "interview_questions": [
    {{"question": "question text", "model_answer": "short model answer"}},
    {{"question": "question text", "model_answer": "short model answer"}},
    {{"question": "question text", "model_answer": "short model answer"}},
    {{"question": "question text", "model_answer": "short model answer"}},
    {{"question": "question text", "model_answer": "short model answer"}}
  ]
}}

Missing skills: {missing_skills}
Weaknesses: {weaknesses}

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