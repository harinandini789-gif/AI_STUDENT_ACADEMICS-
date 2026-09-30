const API = "http://127.0.0.1:5000";


// ---------------- CHATBOT ----------------

async function askQuestion() {

    const input = document.getElementById("chatInput");
    const chatBox = document.getElementById("chatBox");

    const question = input.value.trim();

    if (!question) {
        alert("Please enter a question.");
        return;
    }

    chatBox.innerHTML += `
        <div class="user-message">
            ${question}
        </div>
    `;

    input.value = "";

    try {

        const response = await fetch(`${API}/api/chat`, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                question: question
            })

        });

        const data = await response.json();

        chatBox.innerHTML += `
            <div class="bot-message">
                ${data.answer}
            </div>
        `;

        chatBox.scrollTop = chatBox.scrollHeight;

    } catch (error) {

        chatBox.innerHTML += `
            <div class="bot-message">
                Backend is not running.
                Please start Flask server.
            </div>
        `;
    }
}


// ---------------- PDF UPLOAD ----------------

async function uploadPDF() {

    const fileInput = document.getElementById("pdfFile");
    const status = document.getElementById("uploadStatus");

    if (!fileInput.files.length) {

        alert("Please select a PDF.");

        return;
    }

    const formData = new FormData();

    formData.append(
        "file",
        fileInput.files[0]
    );

    try {

        const response = await fetch(
            `${API}/api/upload`,
            {
                method: "POST",
                body: formData
            }
        );

        const data = await response.json();

        status.innerText = data.message || data.error;

    } catch (error) {

        status.innerText =
            "Unable to connect to backend.";

    }
}


// ---------------- ANSWER GENERATOR ----------------

async function generateAnswer() {

    const topic =
        document.getElementById("answerTopic").value;

    const type =
        document.getElementById("answerType").value;

    if (!topic) {

        alert("Enter a topic.");

        return;
    }

    const response = await fetch(
        `${API}/api/generate-answer`,
        {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                topic: topic,
                type: type
            })

        }
    );

    const data = await response.json();

    document.getElementById(
        "answerResult"
    ).innerText = data.answer;
}


// ---------------- QUIZ ----------------

async function generateQuiz() {

    const topic =
        document.getElementById("quizTopic").value;

    if (!topic) {

        alert("Enter a topic.");

        return;
    }

    const response = await fetch(
        `${API}/api/generate-mcq`,
        {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                topic: topic
            })

        }
    );

    const data = await response.json();

    let html = "";

    data.questions.forEach((q, index) => {

        html += `
            <div class="quiz-question">

                <h3>
                    ${index + 1}. ${q.question}
                </h3>

                <p>A. ${q.options[0]}</p>
                <p>B. ${q.options[1]}</p>
                <p>C. ${q.options[2]}</p>
                <p>D. ${q.options[3]}</p>

                <details>
                    <summary>Show Answer</summary>
                    <strong>${q.answer}</strong>
                </details>

            </div>
        `;

    });

    document.getElementById(
        "quizResult"
    ).innerHTML = html;
}


// ---------------- IMPORTANT QUESTIONS ----------------

async function generateImportantQuestions() {

    const topic =
        document.getElementById(
            "importantTopic"
        ).value;

    if (!topic) {

        alert("Enter a topic.");

        return;
    }

    const response = await fetch(
        `${API}/api/important-questions`,
        {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                topic: topic
            })

        }
    );

    const data = await response.json();

    let html = "<ol>";

    data.questions.forEach(question => {

        html += `
            <li>${question}</li>
        `;

    });

    html += "</ol>";

    document.getElementById(
        "importantResult"
    ).innerHTML = html;
}


// ---------------- SUMMARIZER ----------------

async function summarizeNotes() {

    const text =
        document.getElementById(
            "notesText"
        ).value;

    if (!text) {

        alert("Enter notes.");

        return;
    }

    const response = await fetch(
        `${API}/api/summarize`,
        {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                text: text
            })

        }
    );

    const data = await response.json();

    document.getElementById(
        "summaryResult"
    ).innerText = data.summary;
}


// ---------------- TIMETABLE ----------------

async function createTimetable() {

    const value =
        document.getElementById(
            "subjects"
        ).value;

    const subjects =
        value
        .split(",")
        .map(x => x.trim())
        .filter(x => x);

    if (!subjects.length) {

        alert("Enter subjects.");

        return;
    }

    const response = await fetch(
        `${API}/api/timetable`,
        {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                subjects: subjects
            })

        }
    );

    const data = await response.json();

    let html = "";

    data.timetable.forEach(item => {

        html += `
            <div class="timetable-row">
                <strong>${item.day}</strong>
                <br>
                Subject: ${item.subject}
                <br>
                Time: ${item.time}
            </div>
        `;

    });

    document.getElementById(
        "timetableResult"
    ).innerHTML = html;
}


// ---------------- PROGRESS ----------------

async function updateProgress() {

    const completed =
        document.getElementById(
            "completed"
        ).value;

    const total =
        document.getElementById(
            "total"
        ).value;

    if (!completed || !total) {

        alert("Enter completed and total topics.");

        return;
    }

    const response = await fetch(
        `${API}/api/progress`,
        {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                completed: completed,
                total: total
            })

        }
    );

    const data = await response.json();

    document.getElementById(
        "progressResult"
    ).innerHTML = `
        Completed: ${data.completed}<br>
        Total Topics: ${data.total}<br>
        Progress: <strong>
        ${data.percentage}%
        </strong>
    `;
}


// ---------------- TEXT TO SPEECH ----------------

function speakText() {

    const text =
        document.getElementById(
            "speechText"
        ).value;

    if (!text) {

        alert("Enter text.");

        return;
    }

    const speech =
        new SpeechSynthesisUtterance(text);

    speech.lang = "en-US";

    window.speechSynthesis.speak(
        speech
    );
}


function stopSpeech() {

    window.speechSynthesis.cancel();

}