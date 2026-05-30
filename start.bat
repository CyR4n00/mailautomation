@echo off
echo ==============================================
echo メール自動化・アポ管理ツール 起動スクリプト
echo ==============================================
cd /d "%~dp0"
pip install -r requirements.txt
flask db upgrade
echo.
echo ブラウザで http://127.0.0.1:5000/ にアクセスしてください。
echo.
python run.py
pause
