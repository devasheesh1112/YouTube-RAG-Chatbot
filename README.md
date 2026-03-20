# 🎬 YouTube RAG Chatbot

An AI-powered chatbot that lets you ask questions about any YouTube video using **Retrieval-Augmented Generation (RAG)** with **Google Gemini API**.

---

## 🚀 Demo

> Load any YouTube video → Ask questions → Get AI-powered answers based on the video transcript

---

## 🧠 How It Works

```
YouTube URL
    ↓
Fetch Transcript (youtube-transcript-api)
    ↓
Split into Chunks (LangChain Text Splitter)
    ↓
Embed Chunks (Gemini Embedding API)
    ↓
Store in FAISS Vector Store
    ↓
User asks Question
    ↓
Retrieve Relevant Chunks (Similarity Search)
    ↓
Generate Answer (Gemini LLM)
    ↓
Display in Chat UI
```

---

## 🛠 Tech Stack

| Component       | Technology                        |
|-----------------|-----------------------------------|
| Backend         | Flask (Python)                    |
| LLM             | Google Gemini (gemma-3-4b-it)     |
| Embeddings      | Google Gemini (gemini-embedding-001) |
| Vector Store    | FAISS                             |
| RAG Pipeline    | LangChain LCEL                    |
| Transcripts     | youtube-transcript-api            |
| Frontend        | HTML + CSS + Vanilla JS           |

---

## 📁 Project Structure

```
YouTube-RAG-Chatbot/
├── app.py                  ← Flask app (main entry point)
├── requirements.txt        ← Python dependencies
├── .env                    ← API keys (not pushed)
├── run.bat                 ← One-click run (Windows)
├── src/
│   ├── transcript.py       ← Fetch YouTube transcript
│   ├── indexer.py          ← Split + embed + store in FAISS
│   └── retriever.py        ← RAG chain (retrieve + generate)
├── templates/
│   └── index.html          ← Chat UI
└── static/                 ← Static assets
```

---

## ⚙️ Setup & Run

### 1. Clone the repository
```bash
git clone https://github.com/devasheesh1112/YouTube-RAG-Chatbot.git
cd YouTube-RAG-Chatbot
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up API key
Create a `.env` file in the root folder:
```
GOOGLE_API_KEY=your_google_api_key_here
FLASK_SECRET_KEY=youtube-rag-secret-2024
```
Get your free API key from: [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

### 5. Run the app
```bash
python app.py
```

### 6. Open in browser
```
http://localhost:5000
```

---

## 💬 How to Use

1. Paste any **YouTube video URL**
2. Click **"Load Video"** — transcript is fetched and indexed
3. Ask any question about the video in the chat
4. Get instant AI-powered answers!

---

## 📌 Features

- ✅ Supports any YouTube video with captions
- ✅ Auto-detects available transcript language
- ✅ Hindi transcript auto-translated to English
- ✅ Clean chat UI with message history
- ✅ Powered by Google Gemini (free tier)
- ✅ No data stored permanently

---

## 👨‍💻 Author

**Devasheesh Patidar**
- 🎓 M.Tech CSE — NIT Bhopal
- 💼 [LinkedIn](https://linkedin.com/in/devasheesh-patidar)
- 🐙 [GitHub](https://github.com/devasheesh1112)
