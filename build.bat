
@echo off

echo ==========================================
echo Building Todo App...
echo ==========================================

python -m pip install -r requirements.txt

python -m PyInstaller ^
    --noconfirm ^
    --clean ^
    --windowed ^
    --name "TodoApp" ^
    --add-data "data;data" ^
    main.py

echo.
echo ==========================================
echo Build completed.
echo ==========================================
echo.
echo EXE location:
echo dist\TodoApp\TodoApp.exe
echo.

pause

