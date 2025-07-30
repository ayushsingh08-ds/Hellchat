@echo off
echo 🚀 Starting QWalT - Full Stack Application
echo.

echo 📡 Starting Backend Server (Port 8000)...
start "QWalT Backend" cmd /k "cd /d "%~dp0backend" && python app.py"

timeout /t 3 /nobreak > nul

echo 🎨 Starting Frontend Server (Port 5173)...
start "QWalT Frontend" cmd /k "cd /d "%~dp0frontend" && npm run dev"

timeout /t 5 /nobreak > nul

echo.
echo ✅ Both servers are starting up!
echo.
echo 🔗 Application URLs:
echo    Frontend: http://localhost:5173
echo    Backend:  http://localhost:8000
echo    Health:   http://localhost:8000/health
echo.
echo 📊 Memory Usage: ~69MB (Backend optimized!)
echo.
echo Press any key to open the application in browser...
pause > nul

start http://localhost:5173
