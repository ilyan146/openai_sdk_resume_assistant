@ECHO OFF
echo Activate virtual environment
CALL .\venv\Scripts\activate
echo Starting Database Container
CALL docker compose up monodb -d
echo Starting FastAPI Backend server
cd src/openai_sdk_resume_assistant/backend
CALL uv run uvicorn app.main:app --reload
pause
