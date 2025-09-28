# Simple System Test
Write-Host "Testing WisdomWealth System..." -ForegroundColor Green

# Test 1: Health Check
Write-Host "1. Testing Backend Health..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8000/health"
    Write-Host "✅ Backend is healthy!" -ForegroundColor Green
} catch {
    Write-Host "❌ Backend not responding" -ForegroundColor Red
    exit 1
}

# Test 2: Fraud Agent
Write-Host "2. Testing Fraud Agent..." -ForegroundColor Yellow
$body = @{
    user_id = "test_user"
    text = "Someone called asking for my Social Security number"
    meta = @{}
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/route" -Method POST -ContentType "application/json" -Body $body
    Write-Host "✅ Risk Level: $($response.risk)" -ForegroundColor Green
    Write-Host "✅ Agents: $($response.agent_traces -join ', ')" -ForegroundColor Green
    Write-Host "✅ Response: $($response.response.Substring(0, 100))..." -ForegroundColor Green
} catch {
    Write-Host "❌ Fraud test failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "🎉 Basic tests completed! Open http://localhost:3000 to use the app" -ForegroundColor Green