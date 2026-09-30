from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import re
import random

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024


# ---------------- HOME ----------------

@app.route("/")
def home():
    return jsonify({
        "message": "AI-Based Student Academic Assistant Backend is running"
    })


# ---------------- CHATBOT ----------------

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"answer": "Please enter a question."})

    q = question.lower()

    if "python" in q:
        answer = (
            "Python is a high-level, interpreted programming language. "
            "It is widely used in web development, AI, machine learning, "
            "data science and automation."
        )

    elif "machine learning" in q:
        answer = (
            "Machine Learning is a branch of Artificial Intelligence that "
            "allows computers to learn patterns from data and make predictions "
            "or decisions without being explicitly programmed for every case."
        )

    elif "database" in q:
        answer = (
            "A database is an organized collection of data. "
            "A DBMS is software used to create, store, manage and retrieve "
            "data from databases."
        )

    elif "operating system" in q:
        answer = (
            "An Operating System is system software that manages computer "
            "hardware and software resources and provides services to programs."
        )

    else:
        answer = (
            "I can help you understand academic topics. "
            "For example, ask about Python, Java, DBMS, Operating Systems, "
            "AI, Machine Learning, Computer Networks or other subjects."
        )

    return jsonify({"answer": answer})


# ---------------- PDF / NOTES UPLOAD ----------------

@app.route("/api/upload", methods=["POST"])
def upload_file():

    if "file" not in request.files:
        return jsonify({"error": "No file selected"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Please select a file"}), 400

    filename = secure_filename(file.filename)

    if not filename.lower().endswith(".pdf"):
        return jsonify({"error": "Only PDF files are supported"}), 400

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    return jsonify({
        "message": "PDF uploaded successfully",
        "filename": filename
    })


# ---------------- ANSWER GENERATOR ----------------

@app.route("/api/generate-answer", methods=["POST"])
def generate_answer():

    data = request.get_json()

    topic = data.get("topic", "")
    answer_type = data.get("type", "short")

    if not topic:
        return jsonify({"answer": "Please enter a topic."})

    if answer_type == "short":

        answer = f"""
Short Answer:

{topic} is an important academic concept.

Definition:
{topic} can be understood as a concept used to solve problems and
perform specific operations in its respective field.

Key points:
1. It has a specific purpose.
2. It follows defined principles.
3. It is useful in practical applications.
"""

    else:

        answer = f"""
Long Answer:

Introduction:
{topic} is an important concept in computer science and technology.

Definition:
{topic} refers to a concept or technique used to solve a particular
problem efficiently.

Working:
The concept works by following a sequence of defined steps and
operations.

Advantages:
1. Improves efficiency.
2. Reduces manual work.
3. Can be applied to real-world problems.
4. Provides systematic solutions.

Applications:
{topic} can be used in academic, industrial and software applications.

Conclusion:
Therefore, understanding {topic} is important for both examinations
and practical applications.
"""

    return jsonify({"answer": answer})


# ---------------- MCQ GENERATOR ----------------

@app.route("/api/generate-mcq", methods=["POST"])
def generate_mcq():

    data = request.get_json()
    topic = data.get("topic", "")

    if not topic:
        return jsonify({"error": "Enter a topic"})

    questions = [
        {
            "question": f"What is the main purpose of {topic}?",
            "options": [
                "Solving problems",
                "Playing games",
                "Watching videos",
                "None of these"
            ],
            "answer": "Solving problems"
        },
        {
            "question": f"Which statement about {topic} is correct?",
            "options": [
                "It is useful in technology",
                "It cannot be used practically",
                "It is unrelated to computers",
                "None"
            ],
            "answer": "It is useful in technology"
        },
        {
            "question": f"Where can {topic} be applied?",
            "options": [
                "Academic applications",
                "Industrial applications",
                "Real-world applications",
                "All of the above"
            ],
            "answer": "All of the above"
        }
    ]

    return jsonify({
        "topic": topic,
        "questions": questions
    })


# ---------------- IMPORTANT QUESTIONS ----------------

@app.route("/api/important-questions", methods=["POST"])
def important_questions():

    data = request.get_json()
    topic = data.get("topic", "")

    if not topic:
        return jsonify({"questions": []})

    questions = [
        f"Define {topic} with a suitable example.",
        f"Explain the working of {topic}.",
        f"Discuss the advantages and disadvantages of {topic}.",
        f"Explain the applications of {topic}.",
        f"Compare {topic} with related concepts.",
        f"Explain {topic} with a suitable diagram.",
        f"Write a detailed note on {topic}."
    ]

    return jsonify({"questions": questions})


# ---------------- SUMMARIZER ----------------

@app.route("/api/summarize", methods=["POST"])
def summarize():

    data = request.get_json()
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"summary": "Please enter notes to summarize."})

    sentences = re.split(r'(?<=[.!?])\s+', text)

    summary = " ".join(sentences[:5])

    return jsonify({
        "summary": summary
    })


# ---------------- STUDY TIMETABLE ----------------

@app.route("/api/timetable", methods=["POST"])
def timetable():

    data = request.get_json()

    subjects = data.get("subjects", [])

    if not subjects:
        return jsonify({"error": "Enter subjects"})

    timetable_data = []

    days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday"
    ]

    for i, day in enumerate(days):

        subject = subjects[i % len(subjects)]

        timetable_data.append({
            "day": day,
            "subject": subject,
            "time": "6:00 PM - 7:00 PM"
        })

    return jsonify({
        "timetable": timetable_data
    })


# ---------------- PROGRESS TRACKER ----------------

progress = {
    "completed": 0,
    "total": 0
}


@app.route("/api/progress", methods=["GET"])
def get_progress():

    return jsonify(progress)


@app.route("/api/progress", methods=["POST"])
def update_progress():

    data = request.get_json()

    completed = int(data.get("completed", 0))
    total = int(data.get("total", 0))

    progress["completed"] = completed
    progress["total"] = total

    percentage = 0

    if total > 0:
        percentage = round((completed / total) * 100)

    return jsonify({
        "completed": completed,
        "total": total,
        "percentage": percentage
    })


# ---------------- TEXT TO SPEECH ----------------

@app.route("/api/speech", methods=["POST"])
def speech():

    data = request.get_json()

    text = data.get("text", "")

    if not text:
        return jsonify({"message": "No text provided"})

    return jsonify({
        "message": "Speech request received",
        "text": text
    })


# ---------------- RUN SERVER ----------------

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)