from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from pypdf import PdfReader

import os

# Embedding function
embeddings = OllamaEmbeddings(
    model="mxbai-embed-large"
)

# Store in ChromaDB
resume_db = Chroma(
    collection_name="resume",
    persist_directory="./resume_db",
    embedding_function=embeddings
)

job_db = Chroma(
    collection_name="job",
    persist_directory="./job_db",
    embedding_function=embeddings
)

# Recursively chunk text
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)


def parse_pdf(filepath: str) -> str:
    text = ""
    reader = PdfReader(filepath)

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text

def parse_txt(filepath: str) -> str:

    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def parse_document(filepath: str) -> str:

    if filepath.endswith(".pdf"):
        return parse_pdf(filepath)

    if filepath.endswith(".txt"):
        return parse_txt(filepath)

    raise ValueError(
        f"Unsupported file type: {filepath}"
    )


def create_documents(text: str, source: str):

    chunks = splitter.split_text(text)
    documents = []

    for i, chunk in enumerate(chunks):

        documents.append(
            Document(
                page_content=chunk,
                metadata={
                    "source": source,
                    "chunk": i
                }
            )
        )
    return documents


def ingest_resume(filepath: str):

    text = parse_document(filepath)

    documents = create_documents(
        text=text,
        source=os.path.basename(filepath)
    )

    ids = [
        str(i)
        for i in range(len(documents))
    ]

    resume_db.reset_collection()

    resume_db.add_documents(
        documents=documents,
        ids=ids
    )

    return len(documents)

def ingest_job(filepath: str):

    text = parse_document(filepath)

    documents = create_documents(
        text=text,
        source=os.path.basename(filepath)
    )

    ids = [
        str(i)
        for i in range(len(documents))
    ]

    job_db.reset_collection()

    job_db.add_documents(
        documents=documents,
        ids=ids
    )

    return len(documents)

def retrieve_resume(query: str, k: int = 5):

    return resume_db.similarity_search(
        query=query,
        k=k
    )

def retrieve_job(query: str, k: int = 5):

    return job_db.similarity_search(
        query=query,
        k=k
    )

def get_resume_context(query: str, k: int = 5):

    docs = retrieve_resume(
        query=query,
        k=k
    )

    return "\n\n".join(
        doc.page_content
        for doc in docs
    )

def get_job_context(
    query: str,
    k: int = 5
):

    docs = retrieve_job(
        query=query,
        k=k
    )

    return "\n\n".join(
        doc.page_content
        for doc in docs
    )