@echo off
setlocal

cd /d %~dp0

echo ===== DJANGO AUTO START ===== > debug_log.txt
echo [%date% %time%] START >> debug_log.txt

REM ====== ساخت venv ======
if not exist venv (
    echo Creating venv... >> debug_log.txt
    py -3.10 -m venv venv >> debug_log.txt 2>&1
)

REM ====== استفاده مستقیم از python venv (خیلی مهم) ======
set VENV_PY=venv\Scripts\python.exe

echo Using: %VENV_PY% >> debug_log.txt

REM ====== آپدیت pip داخل venv ======
%VENV_PY% -m pip install --upgrade pip >> debug_log.txt 2>&1

REM ====== نصب requirements داخل venv ======
if exist requirements.txt (
    %VENV_PY% -m pip install -r requirements.txt >> debug_log.txt 2>&1
) else (
    echo requirements.txt NOT FOUND >> debug_log.txt
)

REM ====== تست Django ======
%VENV_PY% -c "import django; print(django.get_version())" >> debug_log.txt 2>&1

REM ====== migrate ======
%VENV_PY% manage.py migrate >> debug_log.txt 2>&1

REM ====== run server ======
start cmd /k %VENV_PY% manage.py runserver

timeout /t 3 > nul
start http://127.0.0.1:8000

echo DONE >> debug_log.txt
endlocal