import streamlit as st
import requests

# ========================================
# Configuration
# ========================================

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Resume Match Analyzer",
    page_icon="📄",
    layout="wide"
)

# ========================================
# Session State
# ========================================

if "resume_uploaded" not in st.session_state:
    st.session_state.resume_uploaded = False

if "job_uploaded" not in st.session_state:
    st.session_state.job_uploaded = False

# ========================================
# Header
# ========================================

st.title("📄 Resume Job Match Analyzer")

st.markdown(
    """
Upload a resume and a job description,
then analyze the candidate match using AI.
"""
)

# ========================================
# Sidebar
# ========================================

with st.sidebar:

    st.header("Upload Documents")

    resume_file = st.file_uploader(
        "Resume",
        type=["pdf", "txt"]
    )

    if st.button("Upload Resume"):

        if resume_file:

            files = {
                "file": (
                    resume_file.name,
                    resume_file,
                    resume_file.type
                )
            }

            response = requests.post(
                f"{BACKEND_URL}/upload_resume",
                files=files
            )

            if response.status_code == 200:

                st.session_state.resume_uploaded = True
                st.success("Resume uploaded successfully.")

            else:

                st.error(response.text)

    if st.session_state.resume_uploaded:
        st.info("✅ Resume loaded")

    st.divider()

    job_file = st.file_uploader(
        "Job Description",
        type=["pdf", "txt"]
    )

    if st.button("Upload Job Description"):

        if job_file:

            files = {
                "file": (
                    job_file.name,
                    job_file,
                    job_file.type
                )
            }

            response = requests.post(
                f"{BACKEND_URL}/upload_job",
                files=files
            )

            if response.status_code == 200:

                st.session_state.job_uploaded = True
                st.success(
                    "Job description uploaded successfully."
                )

            else:

                st.error(response.text)

    if st.session_state.job_uploaded:
        st.info("✅ Job description loaded")

# ========================================
# Match Analysis
# ========================================

st.subheader("🎯 Match Analysis")

if st.button("Analyze Match"):

    # Clear upload messages
    st.session_state.resume_uploaded = False
    st.session_state.job_uploaded = False

    with st.spinner("Analyzing candidate..."):

        response = requests.post(
            f"{BACKEND_URL}/analyze"
        )

        if response.status_code == 200:

            analysis = response.json()["analysis"]

            st.markdown(analysis)

        else:

            st.error(response.text)

# ========================================
# Ask Questions
# ========================================

st.divider()

st.subheader("💬 Ask Questions")

question = st.text_input(
    "Ask anything about the resume or job description"
)

if st.button("Ask Question"):

    # Clear upload messages
    st.session_state.resume_uploaded = False
    st.session_state.job_uploaded = False

    if question:

        with st.spinner("Thinking..."):

            response = requests.post(
                f"{BACKEND_URL}/ask",
                json={
                    "question": question
                }
            )

            if response.status_code == 200:

                data = response.json()

                st.markdown("### Answer")

                st.write(
                    data["answer"]
                )

            else:

                st.error(response.text)

# ========================================
# Footer
# ========================================

st.divider()

st.caption(
    "Powered by FastAPI • ChromaDB • LangChain • Ollama"
)