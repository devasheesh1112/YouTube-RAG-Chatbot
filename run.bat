@echo off
echo ========================================
echo   YouTube RAG Chatbot - Setup and Run
echo ========================================

echo.
echo [1/4] Creating virtual environment...
python -m venv venv

echo.
echo [2/4] Activating virtual environment...
call venv\Scripts\activate

echo.
echo [3/4] Installing / upgrading dependencies...
pip install --upgrade pip
pip install --upgrade youtube-transcript-api
pip install -r requirements.txt

echo.
echo [4/4] Starting Flask app...
echo Open http://localhost:5000 in your browser
echo Press CTRL+C to stop the server
echo.
python app.py

pause
