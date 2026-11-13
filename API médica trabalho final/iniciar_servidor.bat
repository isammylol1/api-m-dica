@echo off
echo ========================================================
echo   Iniciando API Medica de Anamnese e Triagem
echo   Acesse no navegador: http://127.0.0.1:8000
echo ========================================================
python -m uvicorn app.main:app --reload --port 8000
pause
