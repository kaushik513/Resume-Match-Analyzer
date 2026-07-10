const BACKEND_URL = "http://localhost:8000";

// =====================================
// Elements
// =====================================

const resumeInput = document.getElementById("resume-file");
const resumeButton = document.getElementById("upload-resume-btn");
const resumeStatus = document.getElementById("resume-status");

const jobInput = document.getElementById("job-file");
const jobButton = document.getElementById("upload-job-btn");
const jobStatus = document.getElementById("job-status");

const analyzeButton = document.getElementById("analyze-btn");
const analysisResult = document.getElementById("analysis-result");

const askButton = document.getElementById("ask-btn");
const questionInput = document.getElementById("question");
const answerResult = document.getElementById("answer-result");

// =====================================
// Utility
// =====================================

function clearUploadMessages() {
    resumeStatus.textContent = "";
    jobStatus.textContent = "";
}

// =====================================
// Upload Resume
// =====================================

function showLoading(element, message) {
    element.className = "status loading";
    element.textContent = "⏳ " + message;
}

function showSuccess(element, message) {
    element.className = "status success";
    element.textContent = "✅ " + message;
}

function showError(element, message) {
    element.className = "status error";
    element.textContent = "❌ " + message;
}

resumeButton.addEventListener("click", async () => {

    const file = resumeInput.files[0];

    if (!file) {
        resumeStatus.textContent = "Please select a resume file.";
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    showLoading(
    resumeStatus,
    "Uploading resume..."
    );

    try {

        const response = await fetch(
            `${BACKEND_URL}/upload_resume`,
            {
                method: "POST",
                body: formData
            }
        );

        const data = await response.json();

        if (response.ok) {

            showSuccess(
                resumeStatus,
                `Resume uploaded successfully (${data.chunks_created} chunks)`
            );

        } else {

            resumeStatus.textContent =
                `❌ ${data.detail}`;

        }

    } catch (error) {

    console.error(error);

    showError(
        resumeStatus,
        error.message
    );

    }

});

// =====================================
// Upload Job Description
// =====================================

jobButton.addEventListener("click", async () => {

    const file = jobInput.files[0];

    if (!file) {

        jobStatus.textContent =
            "Please select a job description file.";

        return;
    }

    const formData = new FormData();

    formData.append(
        "file",
        file
    );

    showLoading(
        jobStatus,
        "Uploading job description..."
    );

    try {

        const response = await fetch(
            `${BACKEND_URL}/upload_job`,
            {
                method: "POST",
                body: formData
            }
        );

        const data = await response.json();

        if (response.ok) {

            showSuccess(
                jobStatus,
                `Job description uploaded successfully (${data.chunks_created} chunks)`
            );

        } else {

            jobStatus.textContent =
                `❌ ${data.detail}`;

        }

    } catch (error) {

    console.error(error);

    showError(
        resumeStatus,
        error.message
    );

    }

});

// =====================================
// Analyze Match
// =====================================

analyzeButton.addEventListener("click", async () => {

    clearUploadMessages();

    analysisResult.innerHTML =
        `
        <div class="status loading">
        ⏳ Analyzing candidate...
        </div>
        `;

    try {

        const response = await fetch(
            `${BACKEND_URL}/analyze`,
            {
                method: "POST"
            }
        );

        const data = await response.json();

        if (response.ok) {

            analysisResult.innerHTML =
            `
            <div class="status success">
            ✅ Analysis Complete
            </div>  
            <br>
            <pre>${data.analysis}</pre>
            `;

        } else {

            analysisResult.innerText =
                "Analysis failed.";

        }

    } catch (error) {

    console.error(error);

    showError(
        resumeStatus,
        error.message
    );

}

});

// =====================================
// Ask Question
// =====================================

askButton.addEventListener("click", async () => {

    clearUploadMessages();

    const question = questionInput.value.trim();

    if (!question) {

        answerResult.innerText =
            "Please enter a question.";

        return;
    }

    answerResult.innerHTML =
    `
    <div class="status loading">
    ⏳ Generating answer...
    </div>
    `;

    try {

        const response = await fetch(
            `${BACKEND_URL}/ask`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    question: question
                })
            }
        );

        const data = await response.json();

        if (response.ok) {

            answerResult.innerHTML =
            `
            <div class="status success">
            ✅ Answer Generated
            </div>
            <br>
            ${data.answer}
            `;

        } else {

            answerResult.innerText =
                "Question failed.";

        }

    } catch (error) {

    console.error(error);

    showError(
        resumeStatus,
        error.message
    );

}

});