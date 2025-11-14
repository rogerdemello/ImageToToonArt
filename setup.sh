#!/bin/bash

# Image to Cartoon Converter - Setup Script
# This script automates the installation process

echo "🎨 Image to Cartoon Converter - Setup Script"
echo "=============================================="
echo ""

# Check Python installation
echo "📦 Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
else
    echo "❌ Python is not installed. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
echo "✅ Found Python $PYTHON_VERSION"

# Check Node.js installation
echo ""
echo "📦 Checking Node.js installation..."
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 14 or higher."
    exit 1
fi

NODE_VERSION=$(node --version)
echo "✅ Found Node.js $NODE_VERSION"

# Check npm installation
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm."
    exit 1
fi

NPM_VERSION=$(npm --version)
echo "✅ Found npm $NPM_VERSION"

# Create virtual environment
echo ""
echo "🔧 Creating Python virtual environment..."
$PYTHON_CMD -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install Python dependencies
echo ""
echo "📥 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Python dependencies installed successfully"
else
    echo "❌ Failed to install Python dependencies"
    exit 1
fi

# Install frontend dependencies
echo ""
echo "📥 Installing frontend dependencies..."
cd frontend
npm install

if [ $? -eq 0 ]; then
    echo "✅ Frontend dependencies installed successfully"
else
    echo "❌ Failed to install frontend dependencies"
    exit 1
fi

cd ..

# Create necessary directories
echo ""
echo "📁 Creating necessary directories..."
mkdir -p uploads outputs models

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 Next steps:"
echo "1. Start the backend:"
echo "   cd backend"
echo "   python app.py"
echo ""
echo "2. In a new terminal, start the frontend:"
echo "   cd frontend"
echo "   npm start"
echo ""
echo "3. Open http://localhost:3000 in your browser"
echo ""
echo "📚 For more information, see QUICKSTART.md"
