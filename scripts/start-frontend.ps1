# Frontend Setup for WisdomWealth
# Run this in a separate terminal after the backend is running

Write-Host "🌐 WisdomWealth Frontend Setup" -ForegroundColor Green
Write-Host "=============================="

# Check if we're in the right directory
if (-not (Test-Path "wisdomwealth")) {
    Write-Host "❌ Please run this script from the Ackero directory" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "📋 Setting up React Frontend" -ForegroundColor Yellow

# Navigate to web directory
Set-Location "wisdomwealth\web"

# Check if Node.js is installed
try {
    $nodeVersion = node --version 2>$null
    Write-Host "✅ Node.js found: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js not found. Please install Node.js 18+ first" -ForegroundColor Red
    Write-Host "Download from: https://nodejs.org/" -ForegroundColor Cyan
    exit 1
}

# Check if npm is available
try {
    $npmVersion = npm --version 2>$null
    Write-Host "✅ npm found: $npmVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ npm not found. Please install npm" -ForegroundColor Red
    exit 1
}

# Install Node.js dependencies
Write-Host "📦 Installing Node.js dependencies..."
npm install

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install Node.js dependencies" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Node.js dependencies installed successfully" -ForegroundColor Green

# Set environment variable for backend URL
$env:FASTAPI_URL = "http://localhost:8000"

Write-Host ""
Write-Host "🟡 Starting React Development Server..." -ForegroundColor Yellow
Write-Host "Frontend will run on: http://localhost:3000" -ForegroundColor Cyan
Write-Host "Make sure backend is running on: http://localhost:8000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the frontend server" -ForegroundColor Yellow
Write-Host ""

# Start the Vite development server
npm run dev