# Resume Job Match Analyzer

An AI-powered Resume Job Match Analyzer built using FastAPI, Streamlit, LangChain, ChromaDB, and Ollama. This application helps candidates evaluate how well their resume matches a specific job description, identify missing skills, and receive personalized recommendations for improvement.

---

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

### Backend
- FastAPI
- LangChain
- Ollama
- ChromaDB

### Frontend
- Streamlit

### Embeddings
- mxbai-embed-large

### LLM
- Mistral 7B

### Document Processing
- PyPDF
- RecursiveCharacterTextSplitter