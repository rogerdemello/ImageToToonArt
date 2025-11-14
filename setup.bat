@echo off
REM Image to Cartoon Converter - Windows Setup Script

echo 🎨 Image to Cartoon Converter - Setup Script
echo ==============================================
echo.

REM Check Python installation
echo 📦 Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Found Python %PYTHON_VERSION%

REM Check Node.js installation
echo.
echo 📦 Checking Node.js installation...
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed. Please install Node.js 14 or higher.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('node --version') do set NODE_VERSION=%%i
echo ✅ Found Node.js %NODE_VERSION%

REM Check npm installation
npm --version >nul 2>&1
if errorlevel 1 (
    echo ❌ npm is not installed. Please install npm.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('npm --version') do set NPM_VERSION=%%i
echo ✅ Found npm %NPM_VERSION%

REM Create virtual environment
echo.
echo 🔧 Creating Python virtual environment...
python -m venv venv

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install Python dependencies
echo.
echo 📥 Installing Python dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

if errorlevel 1 (
    echo ❌ Failed to install Python dependencies
    pause
    exit /b 1
)

echo ✅ Python dependencies installed successfully

REM Install frontend dependencies
echo.
echo 📥 Installing frontend dependencies...
cd frontend
call npm install

if errorlevel 1 (
    echo ❌ Failed to install frontend dependencies
    pause
    exit /b 1
)

echo ✅ Frontend dependencies installed successfully
cd ..

REM Create necessary directories
echo.
echo 📁 Creating necessary directories...
if not exist uploads mkdir uploads
if not exist outputs mkdir outputs
if not exist models mkdir models

echo.
echo ✅ Setup complete!
echo.
echo 🚀 Next steps:
echo 1. Start the backend:
echo    cd backend
echo    python app.py
echo.
echo 2. In a new terminal, start the frontend:
echo    cd frontend
echo    npm start
echo.
echo 3. Open http://localhost:3000 in your browser
echo.
echo 📚 For more information, see QUICKSTART.md
echo.
pause
