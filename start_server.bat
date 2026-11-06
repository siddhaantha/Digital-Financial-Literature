@echo off
REM start_server.bat — Launch FinSaathi with UTF-8 mode so ₹ and Indian scripts
REM serialise correctly in JSON responses on Windows.
set PYTHONUTF8=1
.\venv\Scripts\python.exe -X utf8 main.py
