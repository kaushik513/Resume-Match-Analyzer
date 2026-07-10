# Resume Job Match Analyzer

An AI-powered Resume Job Match Analyzer built using FastAPI, Streamlit, LangChain, ChromaDB, and Ollama. This application helps candidates evaluate how well their resume matches a specific job description, identify missing skills, and receive personalized recommendations for improvement.


## Features

### Resume and Job Description Upload
Upload in
- PDF format
- TXT format

### Retrieval-Augmented Generation (RAG)
Documents are automatically:
- Parsed
- Chunked using Recursive Character Splitting
- Embedded using Ollama Embeddings
- Stored in ChromaDB

### Match Analysis
Generate:
- Match Score (0–100)
- Matching Skills
- Missing Skills
- Resume Strengths
- Resume Weaknesses
- Hiring Recommendation
- Resume Improvement Suggestions

### Resume Q&A
Ask questions such as:
- What skills am I missing?
- Am I qualified for this role?
- Which projects are most relevant?
- How can I improve my chances of being shortlisted?

## Tech Stack

- Backend: FastAPI, LangChain, Ollama, ChromaDB
- Frontend: HTML, CSS, JavaScript
- Embeddings: mxbai-embed-large
- LLM: Mistral 7B
- Document Processing: PyPDF, RecursiveCharacterTextSplitter

## Project Structure
```text
resume-match-analyzer/
│
├── app.py
├── vector.py
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── uploads/
│
├── resume_db/
│
└── job_db/
```

## How To Run

1. Clone the repository: `git clone https://github.com/kaushik513/Resume-Match-Analyzer`
2. Create empty folders for uploads, resume database and job database as shown in the project structure.
3. Create and activate a virtual environment: 
    - `python -m venv .venv`
    - `.venv\Scripts\Activate.ps1` (on Windows)
4. Install the requirements: `pip install -r requirements.txt`
5. [Install Ollama](https://ollama.com/download) then pull the required models:
    - `ollama pull mistral`
    - `ollama pull mxbai-embed-large`
    - Verify: `ollama list`
6. Run the backend: `fastapi dev app.py`
    - API Documentation: http://localhost:8000/docs
7. Launch the frontend:
    - Right click on index.html
    - Select **Open with Live Server**

## Author
Kaushik Nanduru <br>
Built as a portfolio project to demonstrate end-to-end AI application development using modern LLM, RAG, and full-stack engineering practices.