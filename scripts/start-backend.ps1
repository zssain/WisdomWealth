# Local Testing Setup for WisdomWealth
# Run this script to test the system locally

Write-Host "🚀 WisdomWealth Local Testing Setup" -ForegroundColor Green
Write-Host "=================================="

# Check if we're in the right directory
if (-not (Test-Path "wisdomwealth")) {
    Write-Host "❌ Please run this script from the Ackero directory" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "📋 Step 1: Setting up Python Backend" -ForegroundColor Yellow

# Navigate to agents directory
Set-Location "wisdomwealth\agents"

# Check if Python is installed
try {
    $pythonVersion = python --version 2>$null
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.8+ first" -ForegroundColor Red
    exit 1
}

# Check if pip is available
try {
    pip --version | Out-Null
    Write-Host "✅ pip is available" -ForegroundColor Green
} catch {
    Write-Host "❌ pip not found. Please install pip" -ForegroundColor Red
    exit 1
}

# Install Python dependencies
Write-Host "📦 Installing Python dependencies..."
pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install Python dependencies" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Python dependencies installed successfully" -ForegroundColor Green

# Set environment variables for local testing
$env:GEMINI_API_KEY = "AIzaSyCvJvE7DMeIURv9QN1Lck7xQgFXFa4L_6s"
$env:DATA_DIR = "data"
$env:ENABLE_RETRIEVAL = "true"
$env:PORT = "8000"

Write-Host "✅ Environment variables set" -ForegroundColor Green

# Create data directory if it doesn't exist
if (-not (Test-Path "data")) {
    New-Item -ItemType Directory -Path "data"
    Write-Host "✅ Created data directory" -ForegroundColor Green
}

Write-Host ""
Write-Host "🟡 Starting Python Backend Server..." -ForegroundColor Yellow
Write-Host "Backend will run on: http://localhost:8000" -ForegroundColor Cyan
Write-Host "Health check: http://localhost:8000/health" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the backend server" -ForegroundColor Yellow
Write-Host ""

# Start the FastAPI server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload