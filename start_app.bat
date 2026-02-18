@echo off
echo ================================
echo  AI Analytics App Launcher
echo ================================

cd /d "%~dp0"

powershell -Command "Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass"

call venv\Scripts\activate

start cmd /k "ollama serve"

timeout /t 5

streamlit run app.py

pause
