from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel

from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

from vector import (
ingest_resume,
    ingest_job,
    get_resume_context,
    get_job_context
)

import os
import shutil

app = FastAPI(
    title="Resume Job Match Analyzer",
    version="1.0.0"
)

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)

llm = OllamaLLM(
    model="mistral"
)

class QuestionRequest(BaseModel):
    question: str


@app.post("/upload_resume")
async def upload_resume(file: UploadFile = File(...)):

    if not (
        file.filename.endswith(".pdf")
        or file.filename.endswith(".txt")
    ):
        raise HTTPException(
            status_code=400,
            detail="Only PDF and TXT files are supported."
        )

    filepath = os.path.join(
        UPLOAD_DIR,
        f"resume_{file.filename}"
    )

    with open(
        filepath,
        "wb"
    ) as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    chunk_count = ingest_resume(filepath)

    return {
        "message": "Resume uploaded successfully",
        "chunks_created": chunk_count
    }


@app.post("/upload_job")
async def upload_job(file: UploadFile = File(...)):

    if not (
        file.filename.endswith(".pdf")
        or file.filename.endswith(".txt")
    ):
        raise HTTPException(
            status_code=400,
            detail="Only PDF and TXT files are supported."
        )

    filepath = os.path.join(
        UPLOAD_DIR,
        f"job_{file.filename}"
    )

    with open(
        filepath,
        "wb"
    ) as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    chunk_count = ingest_job(filepath)

    return {
        "message": "Job description uploaded successfully",
        "chunks_created": chunk_count
    }

# ==================================================
# Analyze Candidate Match
# ==================================================

@app.post("/analyze")
def analyze_match():

    resume_context = get_resume_context(
        query="skills experience education projects"
    )

    job_context = get_job_context(
        query="required skills qualifications duties responsibilities"
    )

    template = """
You are a senior technical recruiter.

Compare the candidate's resume against the job description.

Resume:
{resume}

Job Description:
{job}

Return the analysis in exactly this format:

MATCH SCORE:
<number>/100

MATCHING SKILLS:
- item
- item

MISSING SKILLS:
- item
- item

STRENGTHS:
- item
- item

WEAKNESSES:
- item
- item

HIRING RECOMMENDATION:
<recommendation>

RESUME IMPROVEMENTS:
- item
- item
"""

    prompt = ChatPromptTemplate.from_template(
        template
    )

    chain = prompt | llm

    result = chain.invoke(
        {
            "resume": resume_context,
            "job": job_context
        }
    )

    return {
        "analysis": result
    }

# ==================================================
# Ask Questions
# ==================================================

@app.post("/ask")
def ask_question(
    request: QuestionRequest
):

    resume_context = get_resume_context(
        request.question
    )

    job_context = get_job_context(
        request.question
    )

    template = """
Answer the question using both the resume and job description.

Resume:
{resume}

Job Description:
{job}

Question:
{question}

If the answer cannot be determined from the documents,
state that clearly.
"""

    prompt = ChatPromptTemplate.from_template(
        template
    )

    chain = prompt | llm

    result = chain.invoke(
        {
            "resume": resume_context,
            "job": job_context,
            "question": request.question
        }
    )

    return {
        "question": request.question,
        "answer": result
    }

# ==================================================
# Health Check
# ==================================================

@app.get("/")
def home():

    return {
        "status": "running",
        "llm": "mistral"
    }