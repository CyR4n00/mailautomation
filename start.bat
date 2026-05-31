@echo off
chcp 65001 >nul
setlocal
echo ==============================================
echo メール自動化・アポ管理ツール 起動スクリプト
echo ==============================================

cd /d "%~dp0"

echo [1/3] Pythonの依存関係を確認しています...
pip install -r requirements.txt
if %ERRORLEVEL% neq 0 goto ERROR_END

echo [2/3] データベースをセットアップしています...
if not exist "instance\app.db" (
    flask db upgrade
    if %ERRORLEVEL% neq 0 goto ERROR_END
)

echo.
echo ==============================================
echo 起動の準備が完了しました。
echo ブラウザで以下のURLにアクセスしてください。
echo http://127.0.0.1:5000/
echo.
echo ※ツールを終了する場合は、この黒いウィンドウを閉じてください。
echo ==============================================
echo.

python run.py

if %ERRORLEVEL% neq 0 goto ERROR_END
goto END

:ERROR_END
echo.
echo エラーが発生したため起動を中止しました。
echo 上記のエラーメッセージを確認してください。
pause

:END
