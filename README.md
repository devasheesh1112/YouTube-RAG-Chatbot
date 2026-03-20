# YouTube RAG Chatbot 🎬

An AI-powered chatbot that lets you ask questions about any YouTube video using **LangChain**, **Google Gemini**, and **RAG (Retrieval-Augmented Generation)**.

---

## 📁 Folder Structure

```
YouTube-RAG-Chatbot/
├── app.py                  # Flask web app (main entry point)
├── requirements.txt        # Python dependencies
├── .env.example            # Example env file (copy to .env)
├── run.bat                 # Double-click to run on Windows
├── reinstall.bat           # Reinstall all packages
├── README.md               # Documentation
├── src/
│   ├── transcript.py       # Fetch YouTube transcript
│   ├── indexer.py          # Split text + build FAISS vectorstore
│   └── retriever.py        # RAG QA chain using LangChain + Gemini
├── templates/
│   └── index.html          # Frontend chat UI
├── static/                 # CSS/JS assets
└── data/                   # FAISS index (auto-generated)
```

---

## ⚙️ Setup & Run

### 1. Clone the repo
```bash
git clone https://github.com/devasheesh1112/YouTube-RAG-Chatbot.git
cd YouTube-RAG-Chatbot
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your Google Gemini API Key
```bash
cp .env.example .env
```
Open `.env` and add your key:
```
GOOGLE_API_KEY=your_google_api_key_here
```
Get free key from: https://aistudio.google.com/app/apikey

### 5. Run the app
```bash
python app.py
```

### 6. Open in browser
```
http://localhost:5000
```

---

## 🚀 How to Use

1. Paste a **YouTube video URL**
2. Click **Load Video** — fetches transcript and builds index
3. Ask any question about the video in the chat!

---

## 🛠 Tech Stack

| Component     | Technology                        |
|---------------|-----------------------------------|
| Backend       | Flask (Python)                    |
| LLM           | Google Gemini (gemma-3-4b-it)     |
| Embeddings    | Google Gemini (gemini-embedding-001) |
| Vector Store  | FAISS                             |
| RAG Pipeline  | LangChain LCEL                    |
| Transcripts   | youtube-transcript-api            |
| Frontend      | HTML + CSS + Vanilla JS           |

---

## 📝 Notes
- Video must have captions/transcript enabled
- Supports Hindi and English transcripts
- Free tier API key from Google AI Studio works
