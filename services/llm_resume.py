# import groq
# import json
# from core.config import GROQ_API_KEY  # You must add GROQ_API_KEY to your .env

# # Configure Groq API key
# groq_client = groq.Client(api_key=GROQ_API_KEY)

# def analyze_resume(resume_text, job_description):
#     prompt = f"""
# You are a technical HR expert hiring for multiple roles. You evaluate resumes based on job requirements,
# skills, and work experience. You also help candidates rewrite their resume to align with the job description.

# Given:
# - Job Description: {job_description}
# - Candidate's Resume: {resume_text}

# Tasks:
# 1. Rate match percentage (0-100%).
# 2. List missing skills.
# 3. Rewrite the resume optimized for the job.

# Respond STRICTLY in JSON format like:
# {{
#   "Similarity_percentages": 84,
#   "Missing_skills": ["Docker", "AWS"],
#   "Optimized_resume": "Optimized resume here..."
# }}
# """

#     try:
#         response = groq_client.chat.completions.create(
#             model="llama-3.1-8b-instant",  # You can use llama3-8b-8192 or mixtral-8x7b-32768 based on your quota
#             messages=[
#                 {"role": "system", "content": "You are an expert career consultant."},
#                 {"role": "user", "content": prompt}
#             ],
#             temperature=0.2
#         )

#         reply_text = response.choices[0].message.content
#         return json.loads(reply_text)

#     except Exception as e:
#         return {"error": "Failed to process LLM response", "details": str(e)}


# import groq
# import json
# import re
# from core.config import GROQ_API_KEY

# groq_client = groq.Client(api_key=GROQ_API_KEY)

# def extract_json(text):
#     """
#     Extracts JSON block from LLM response safely, even if wrapped in markdown or has formatting issues.
#     """
#     match = re.search(r'\{.*\}', text, re.DOTALL)
#     if match:
#         json_text = match.group(0)
#         # Fix common issues: Remove raw line breaks inside strings
#         json_text = re.sub(r'(?<!\\)\n', '\\n', json_text)
#         return json_text
#     return None

# def analyze_resume(resume_text, job_description):
#     prompt = f"""
# You are a technical HR expert hiring for multiple roles. You evaluate resumes based on job requirements,
# skills, and work experience. You also help candidates rewrite their resume to align with the job description.

# Given:
# - Job Description: {job_description}
# - Candidate's Resume: {resume_text}

# Tasks:
# 1. Rate match percentage (0-100%).
# 2. List missing skills.
# 3. Rewrite the resume optimized for the job.

# Example Output:
# {{
#   "Similarity_percentages": 84,
#   "Missing_skills": ["Docker", "AWS"],
#   "Optimized_resume": "Optimized resume here..."
# }}

# IMPORTANT: Return only raw JSON, no markdown, no explanations.
# """

#     try:
#         response = groq_client.chat.completions.create(
#             model="llama-3.1-8b-instant",
#             messages=[
#                 {"role": "system", "content": "You are an expert career consultant."},
#                 {"role": "user", "content": prompt}
#             ],
#             temperature=0.2
#         )

#         reply_text = response.choices[0].message.content
#         print("🔧 RAW LLM RESPONSE:")
#         print(repr(reply_text))

#         #print("RAW LLM RESPONSE:", repr(reply_text))  # Debug output

#         json_text = extract_json(reply_text)
#         if not json_text:
#             raise ValueError("No valid JSON found in LLM response.")

#         return json.loads(json_text)

#     except Exception as e:
#         return {"error": "Failed to process LLM response", "details": str(e)}


import groq
import json
import re
from core.config import GROQ_API_KEY

groq_client = groq.Client(api_key=GROQ_API_KEY)

def extract_json(text):
    """
    Extract JSON from LLM response, sanitize line breaks for safe parsing.
    """
    # Remove markdown code wrappers
    text = text.replace("```json", "").replace("```", "").strip()

    # Find JSON block
    start = text.find("{")
    end = text.rfind("}") + 1
    if start == -1 or end == -1:
        return None

    json_text = text[start:end]

    # Replace raw newlines and tabs inside strings with escaped versions
    json_text = re.sub(r'(?<!\\)\n', '\\n', json_text)
    json_text = re.sub(r'(?<!\\)\t', '\\t', json_text)

    return json_text

def analyze_resume(resume_text, job_description):
    prompt = f"""
You are a technical HR expert hiring for multiple roles. You evaluate resumes based on job requirements,
skills, and work experience. You also help candidates rewrite their resume to align with the job description.

TASK:
- Given Job Description and Resume
- Rate similarity (0-100)
- List missing skills
- Rewrite optimized resume

Output JSON ONLY:
{{
  "Similarity_percentages": 85,
  "Missing_skills": ["Docker", "AWS"],
  "Optimized_resume": "One-line updated resume with \\n for line breaks"
}}

IMPORTANT:
- Escape all line breaks as \\n
- No markdown, no extra text, pure valid JSON only
"""


    try:
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are an expert career consultant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0
        )

        reply_text = response.choices[0].message.content
        print("🔧 RAW LLM RESPONSE:", repr(reply_text))

        json_text = extract_json(reply_text)
        if not json_text:
            return {"error": "No valid JSON found in LLM response.", "raw_llm": reply_text}

        parsed = json.loads(json_text)
        parsed["raw_llm"] = reply_text  # Include raw for debugging
        return parsed

    except Exception as e:
        return {"error": "Failed to process LLM response.", "details": str(e)}
