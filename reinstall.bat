@echo off
echo ========================================
echo   Cleaning and Reinstalling All Packages
echo ========================================

call venv\Scripts\activate

echo.
echo [1/5] Uninstalling old packages...
pip uninstall openai langchain langchain-openai langchain-community langchain-core tiktoken faiss-cpu -y

echo.
echo [2/5] Clearing pip cache...
pip cache purge

echo.
echo [3/5] Upgrading pip...
python -m pip install --upgrade pip

echo.
echo [4/5] Installing all packages fresh...
pip install flask==3.0.0
pip install openai==1.12.0
pip install tiktoken==0.7.0
pip install langchain==0.2.16
pip install langchain-core==0.2.38
pip install langchain-openai==0.1.23
pip install langchain-community==0.2.16
pip install faiss-cpu==1.7.4
pip install youtube-transcript-api==1.2.4
pip install python-dotenv==1.0.1
pip install requests==2.31.0

echo.
echo [5/5] Verifying installations...
python -c "import flask; print('flask OK:', flask.__version__)"
python -c "import openai; print('openai OK:', openai.__version__)"
python -c "import langchain; print('langchain OK:', langchain.__version__)"
python -c "import langchain_openai; print('langchain_openai OK')"
python -c "import langchain_community; print('langchain_community OK')"
python -c "import faiss; print('faiss OK')"
python -c "import youtube_transcript_api; print('youtube_transcript_api OK')"

echo.
echo ========================================
echo   All done! Now run: python app.py
echo ========================================
pause
