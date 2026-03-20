import os
from flask import Flask, render_template, request, jsonify
from src.transcript import get_transcript
from src.indexer import split_text, build_vectorstore
from src.retriever import build_qa_chain, get_answer
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "rag-secret-key-2024")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

qa_chains = {}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/load", methods=["POST"])
def load_video():
    if not GOOGLE_API_KEY:
        return jsonify({
            "error": "Google API key not found. Please add GOOGLE_API_KEY=your_key to your .env file."
        }), 400

    data = request.get_json()
    url = data.get("url", "").strip()

    if not url:
        return jsonify({"error": "Please provide a YouTube URL."}), 400

    try:
        transcript = get_transcript(url)
        docs = split_text(transcript)
        vectorstore = build_vectorstore(docs, GOOGLE_API_KEY)
        qa_chain = build_qa_chain(vectorstore, GOOGLE_API_KEY)

        session_id = request.remote_addr
        qa_chains[session_id] = qa_chain

        return jsonify({
            "success": True,
            "message": f"Video loaded! Transcript split into {len(docs)} chunks. Ready to chat."
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "").strip()

    session_id = request.remote_addr
    qa_chain = qa_chains.get(session_id)

    if not qa_chain:
        return jsonify({"error": "No video loaded. Please load a YouTube video first."}), 400
    if not question:
        return jsonify({"error": "Please enter a question."}), 400

    try:
        answer = get_answer(qa_chain, question)
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
