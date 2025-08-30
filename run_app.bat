@echo off
echo Starting the application...
call .\venv\Scripts\activate
set FLASK_APP=run.py
set FLASK_ENV=development
flask run
pause
