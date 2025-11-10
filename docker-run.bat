@echo off
REM Docker Container Management Script for Windows
REM CSE_proj_12 - Phishing Detection

echo ======================================================================
echo 🐳 Phishing Detection - Docker Container Manager
echo ======================================================================

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not running. Please start Docker Desktop.
    pause
    exit /b 1
)
echo ✓ Docker is running

:menu
echo.
echo ======================================================================
echo Select an option:
echo ======================================================================
echo 1. Build and Run (Full Setup)
echo 2. Build Image Only
echo 3. Run Container
echo 4. Stop Container
echo 5. View Logs
echo 6. Access Shell
echo 7. Use Docker Compose
echo 8. Exit
echo ======================================================================
set /p choice="Enter choice [1-8]: "

if "%choice%"=="1" goto full
if "%choice%"=="2" goto build
if "%choice%"=="3" goto run
if "%choice%"=="4" goto stop
if "%choice%"=="5" goto logs
if "%choice%"=="6" goto shell
if "%choice%"=="7" goto compose
if "%choice%"=="8" goto end
echo Invalid option
goto menu

:build
echo.
echo ======================================================================
echo 🔨 Building Docker Image...
echo ======================================================================
docker build -t phishing-detection-api -f .devcontainer/Dockerfile .
echo ✓ Image built successfully
goto menu

:run
echo.
echo ======================================================================
echo 🚀 Starting Container...
echo ======================================================================

REM Stop existing container if running
docker stop phishing-api 2>nul
docker rm phishing-api 2>nul

REM Run new container
docker run -d ^
    --name phishing-api ^
    -p 8000:8000 ^
    -v "%cd%":/workspace ^
    -w /workspace ^
    phishing-detection-api ^
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

echo ✓ Container started successfully
echo.
echo 📍 API available at:
echo    • http://localhost:8000
echo    • http://localhost:8000/docs (Swagger UI)
echo.
echo 📋 Useful commands:
echo    • View logs:    docker logs -f phishing-api
echo    • Stop:         docker stop phishing-api
echo    • Restart:      docker restart phishing-api
echo    • Shell access: docker exec -it phishing-api bash
goto menu

:stop
echo.
echo ======================================================================
echo 🛑 Stopping Container...
echo ======================================================================
docker stop phishing-api 2>nul
docker rm phishing-api 2>nul
echo ✓ Container stopped
goto menu

:logs
echo.
echo ======================================================================
echo 📋 Container Logs (Press Ctrl+C to exit)
echo ======================================================================
docker logs -f phishing-api
goto menu

:shell
echo.
echo ======================================================================
echo 🖥️  Accessing Container Shell
echo ======================================================================
docker exec -it phishing-api bash
goto menu

:compose
echo.
echo ======================================================================
echo 🐳 Using Docker Compose...
echo ======================================================================
docker-compose up --build
goto menu

:full
call :build
call :run
goto menu

:end
echo Goodbye!
pause
exit /b 0
