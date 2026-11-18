@echo off
echo ========================================================
echo Starting FastAPI Backend Server (SmartOps Intelligence)
echo ========================================================
set DISABLE_SQLALCHEMY_CEXT=1
python -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000 --reload
pause
