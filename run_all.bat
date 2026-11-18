@echo off
echo =========================================================================
echo Launching AI-Powered Smart Business Operations & Decision Intelligence
echo =========================================================================
start "FastAPI Backend" run_backend.bat
start "React.js Frontend" run_frontend.bat
echo Both services are booting up!
echo Backend:  http://localhost:8000 (Swagger: http://localhost:8000/docs)
echo Frontend: http://localhost:3000
