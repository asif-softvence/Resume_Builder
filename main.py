# from fastapi import FastAPI, Query
# import os
# import dotenv
# import requests

# # Load environment variables from .env file
# dotenv.load_dotenv()

# app = FastAPI()

# # Get your actual API key from environment variables
# API_KEY = os.getenv("JSEARCH_API_KEY")
# HOST = "jsearch.p.rapidapi.com"


# @app.get("/jobs")
# def search_jobs(query: str = Query(...), location: str = Query(...), page: int = 1):
#     URL = "https://jsearch.p.rapidapi.com/search"

#     headers = {
#         "X-RapidAPI-Key": API_KEY,
#         "X-RapidAPI-Host": HOST
#     }

#     params = {
#         "query": f"{query} in {location}",
#         "page": page,
#         "num_pages": 1
#     }

#     response = requests.get(URL, headers=headers, params=params)

#     if response.status_code == 200:
#         return response.json()
#     return {"error": response.text}




from fastapi import FastAPI, UploadFile, Form, Query, HTTPException
from fastapi.responses import JSONResponse
from services.fetch_job import fetch_job
from services.llm_resume import analyze_resume
from services.pdf_reader import read_pdf_text

app = FastAPI(title="LLM Resume Matcher & Builder")

# --- 1. Fetch Jobs ---
@app.get("/jobs")
def search_jobs(query: str = Query(...), location: str = Query(...), page: int = 1):
    return fetch_job(query, location, page)


# --- 2. Resume Upload & Match ---
# @app.post("/match-resume/")
# async def match_resume(
#     resume_file: UploadFile,
#     job_description: str = Form(...)
# ):
#     content = await resume_file.read()
#     resume_text = (
#         read_pdf_text(content) if resume_file.filename.endswith(".pdf") else content.decode("utf-8")
#     )

@app.post("/match-resume/")
async def match_resume(resume_file: UploadFile, job_description: str = Form(...)):
    content = await resume_file.read()
    resume_text = read_pdf_text(content) if resume_file.filename.endswith(".pdf") else content.decode("utf-8")

    result = analyze_resume(resume_text, job_description)
    return result

    # try:
    #     result = analyze_resume(resume_text, job_description)
    #     return JSONResponse(content=result)
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))
