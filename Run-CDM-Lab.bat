@echo off
cd /d %~dp0
echo ==========================================
echo  Cyber Defense Matrix: AI Automation Lab
echo ==========================================
echo Initializing local environment...

if not exist .venv (
    echo Creating Python virtual environment...
    python -m venv .venv
)

call .venv\Scripts\activate
echo Checking dependencies...
pip install -r requirements.txt /Q

echo.
echo Launching dashboard in your browser...
echo Close this window to stop the application.
echo ==========================================
streamlit run app.py
pause