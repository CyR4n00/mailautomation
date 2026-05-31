@echo off
cd /d "%~dp0"

echo [1/3] Installing requirements...
python -m pip install -r requirements.txt

echo [2/3] Setting up database...
python -m flask db upgrade

echo [3/3] Starting server...
echo Please open http://127.0.0.1:5000/ in your browser.
python run.py

pause
