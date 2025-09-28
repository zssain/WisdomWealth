# Quick test script for WisdomWealth backend
# Make sure backend is running first (python start-backend.ps1)

Write-Host "🧪 Testing WisdomWealth Backend" -ForegroundColor Green
Write-Host "==============================="

$backendUrl = "http://localhost:8000"

# Test 1: Health Check
Write-Host ""
Write-Host "🔍 Test 1: Health Check" -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$backendUrl/health" -Method GET -TimeoutSec 10
    Write-Host "✅ Health check passed" -ForegroundColor Green
    Write-Host "   Status: $($response.status)" -ForegroundColor Cyan
    Write-Host "   Agents: $($response.agents | ConvertTo-Json -Compress)" -ForegroundColor Cyan
    Write-Host "   Database: $($response.database | ConvertTo-Json -Compress)" -ForegroundColor Cyan
} catch {
    Write-Host "❌ Health check failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "   Make sure backend is running: python start-backend.ps1" -ForegroundColor Yellow
    exit 1
}

# Test 2: Simple fraud detection
Write-Host ""
Write-Host "🔍 Test 2: Fraud Detection" -ForegroundColor Yellow
try {
    $testData = @{
        user_id = "test_user_$(Get-Date -Format 'HHmmss')"
        text = "Someone called asking for my Social Security number"
        meta = @{ test = $true }
    }
    
    $headers = @{
        "Content-Type" = "application/json"
    }
    
    $response = Invoke-RestMethod -Uri "$backendUrl/route" -Method POST -Body ($testData | ConvertTo-Json) -Headers $headers -TimeoutSec 30
    
    Write-Host "✅ Fraud detection test passed" -ForegroundColor Green
    Write-Host "   Risk Level: $($response.risk)" -ForegroundColor Cyan
    Write-Host "   Agents: $($response.agent_traces -join ', ')" -ForegroundColor Cyan
    Write-Host "   Response: $($response.response.Substring(0, [Math]::Min(80, $response.response.Length)))..." -ForegroundColor Cyan
    Write-Host "   Actions: $($response.actions -join ', ')" -ForegroundColor Cyan
    
} catch {
    Write-Host "❌ Fraud detection test failed: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.Exception.Response) {
        Write-Host "   Status: $($_.Exception.Response.StatusCode)" -ForegroundColor Red
    }
    exit 1
}

# Test 3: Healthcare query
Write-Host ""
Write-Host "🔍 Test 3: Healthcare Query" -ForegroundColor Yellow
try {
    $testData = @{
        user_id = "test_user_$(Get-Date -Format 'HHmmss')"
        text = "I received a $2000 hospital bill that seems too high"
        meta = @{ test = $true }
    }
    
    $response = Invoke-RestMethod -Uri "$backendUrl/route" -Method POST -Body ($testData | ConvertTo-Json) -Headers $headers -TimeoutSec 30
    
    Write-Host "✅ Healthcare query test passed" -ForegroundColor Green
    Write-Host "   Risk Level: $($response.risk)" -ForegroundColor Cyan
    Write-Host "   Agents: $($response.agent_traces -join ', ')" -ForegroundColor Cyan
    Write-Host "   Actions: $($response.actions -join ', ')" -ForegroundColor Cyan
    
} catch {
    Write-Host "❌ Healthcare query test failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 4: Stats endpoint
Write-Host ""
Write-Host "🔍 Test 4: Stats Endpoint" -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$backendUrl/stats" -Method GET -TimeoutSec 10
    Write-Host "✅ Stats endpoint test passed" -ForegroundColor Green
    Write-Host "   Total incidents: $($response.database.total_users)" -ForegroundColor Cyan
    
} catch {
    Write-Host "⚠️ Stats endpoint test failed: $($_.Exception.Message)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🎉 Backend Testing Complete!" -ForegroundColor Green
Write-Host "Ready to test the frontend at: http://localhost:3000" -ForegroundColor Cyan
Write-Host "Run: powershell .\start-frontend.ps1" -ForegroundColor Yellow