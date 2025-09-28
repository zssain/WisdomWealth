# WisdomWealth System Test Script
# Tests all agents with comprehensive scenarios

Write-Host "🚀 Starting WisdomWealth System Tests..." -ForegroundColor Green
Write-Host "=" * 50

$baseUrl = "http://localhost:8000"
$testResults = @()

function Test-Agent {
    param(
        [string]$TestName,
        [string]$Message,
        [string]$ExpectedRisk,
        [string[]]$ExpectedAgents
    )
    
    Write-Host "🧪 Testing: $TestName" -ForegroundColor Cyan
    
    try {
        $body = @{
            user_id = "test_user_$(Get-Date -Format 'HHmmss')"
            text = $Message
            meta = @{}
        } | ConvertTo-Json
        
        $response = Invoke-RestMethod -Uri "$baseUrl/route" -Method POST -ContentType "application/json" -Body $body -TimeoutSec 30
        
        $result = @{
            TestName = $TestName
            Success = $true
            Risk = $response.risk
            Agents = $response.agent_traces
            Response = $response.response
            Confidence = $response.confidence_score
            Actions = $response.actions
        }
        
        # Validate expected risk level
        if ($response.risk -eq $ExpectedRisk.ToLower()) {
            Write-Host "  ✅ Risk Level: $($response.risk) (Expected: $($ExpectedRisk.ToLower()))" -ForegroundColor Green
        } else {
            Write-Host "  ❌ Risk Level: $($response.risk) (Expected: $($ExpectedRisk.ToLower()))" -ForegroundColor Red
        }
        
        # Validate expected agents
        $foundAgents = $response.agent_traces
        foreach ($expectedAgent in $ExpectedAgents) {
            if ($foundAgents -contains $expectedAgent) {
                Write-Host "  ✅ Agent: $expectedAgent activated" -ForegroundColor Green
            } else {
                Write-Host "  ❌ Agent: $expectedAgent NOT activated" -ForegroundColor Red
            }
        }
        
        Write-Host "  📊 Confidence: $($response.confidence_score)" -ForegroundColor Yellow
        Write-Host "  🎯 Actions: $($response.actions -join ', ')" -ForegroundColor Yellow
        Write-Host "  💬 Response: $($response.response.Substring(0, [Math]::Min(100, $response.response.Length)))..." -ForegroundColor Gray
        
    } catch {
        Write-Host "  ❌ Test Failed: $($_.Exception.Message)" -ForegroundColor Red
        $result = @{
            TestName = $TestName
            Success = $false
            Error = $_.Exception.Message
        }
    }
    
    $testResults += $result
    Write-Host ""
    Start-Sleep -Seconds 2
}

# Test if backend is running
Write-Host "🔍 Checking backend health..." -ForegroundColor Yellow
try {
    $healthCheck = Invoke-RestMethod -Uri "$baseUrl/health" -TimeoutSec 10
    Write-Host "✅ Backend is healthy!" -ForegroundColor Green
} catch {
    Write-Host "❌ Backend not responding. Please start with: .\scripts\start-backend.ps1" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🛡️ FRAUD PROTECTION AGENT TESTS" -ForegroundColor Blue
Write-Host "=" * 40

Test-Agent -TestName "SSN Phone Scam" `
    -Message "Someone called saying they're from the IRS and need my Social Security number to avoid arrest" `
    -ExpectedRisk "high" `
    -ExpectedAgents @("fraud", "family")

Test-Agent -TestName "Gift Card Scam" `
    -Message "A caller said I owe money and must pay with gift cards immediately" `
    -ExpectedRisk "high" `
    -ExpectedAgents @("fraud", "family")

Test-Agent -TestName "Grandparent Scam" `
    -Message "Someone called saying my grandson is in jail and needs 5000 dollars bail money right now" `
    -ExpectedRisk "high" `
    -ExpectedAgents @("fraud", "family")

Test-Agent -TestName "Tech Support Scam" `
    -Message "Microsoft called about a virus on my computer and wants remote access" `
    -ExpectedRisk "high" `
    -ExpectedAgents @("fraud", "family")

Write-Host "💚 HEALTHCARE FINANCE AGENT TESTS" -ForegroundColor Blue
Write-Host "=" * 40

Test-Agent -TestName "High Medical Bill" `
    -Message "I received a 15000 dollar hospital bill but I have insurance, why is it so high?" `
    -ExpectedRisk "medium" `
    -ExpectedAgents @("healthcare")

Test-Agent -TestName "Insurance Denial" `
    -Message "My insurance denied coverage for my surgery, what should I do?" `
    -ExpectedRisk "medium" `
    -ExpectedAgents @("healthcare")

Test-Agent -TestName "Medicare Question" `
    -Message "I need help choosing between Medicare Plan A and Plan B" `
    -ExpectedRisk "low" `
    -ExpectedAgents @("healthcare")

Write-Host "📋 ESTATE PLANNING AGENT TESTS" -ForegroundColor Blue
Write-Host "=" * 40

Test-Agent -TestName "Will Creation" `
    -Message "I need to create a will but don't know where to start" `
    -ExpectedRisk "low" `
    -ExpectedAgents @("estate")

Test-Agent -TestName "Document Organization" `
    -Message "Help me organize my important financial documents" `
    -ExpectedRisk "low" `
    -ExpectedAgents @("estate")

Test-Agent -TestName "Power of Attorney" `
    -Message "I want to set up a power of attorney for my daughter" `
    -ExpectedRisk "low" `
    -ExpectedAgents @("estate")

Write-Host "👥 FAMILY COORDINATION AGENT TESTS" -ForegroundColor Blue
Write-Host "=" * 40

Test-Agent -TestName "Emergency Contact" `
    -Message "I fell and need someone to contact my family" `
    -ExpectedRisk "high" `
    -ExpectedAgents @("family")

Test-Agent -TestName "Hospital Notification" `
    -Message "I'm in the hospital and need my daughter notified" `
    -ExpectedRisk "medium" `
    -ExpectedAgents @("family")

Write-Host "🔄 MULTI-AGENT TESTS" -ForegroundColor Blue
Write-Host "=" * 40

Test-Agent -TestName "Medical Bill Scam" `
    -Message "I got a call about a medical bill I don't remember, they want me to pay over the phone with a credit card" `
    -ExpectedRisk "high" `
    -ExpectedAgents @("fraud", "healthcare", "family")

Test-Agent -TestName "Insurance Scam" `
    -Message "Someone claiming to be from my insurance company wants my Medicare number to process a refund" `
    -ExpectedRisk "high" `
    -ExpectedAgents @("fraud", "healthcare", "family")

# Generate Summary Report
Write-Host "📊 TEST SUMMARY REPORT" -ForegroundColor Green
Write-Host "=" * 50

$totalTests = $testResults.Count
$passedTests = ($testResults | Where-Object { $_.Success -eq $true }).Count
$failedTests = $totalTests - $passedTests

Write-Host "Total Tests: $totalTests" -ForegroundColor White
Write-Host "Passed: $passedTests" -ForegroundColor Green
Write-Host "Failed: $failedTests" -ForegroundColor Red

if ($failedTests -gt 0) {
    Write-Host ""
    Write-Host "❌ Failed Tests:" -ForegroundColor Red
    $testResults | Where-Object { $_.Success -eq $false } | ForEach-Object {
        Write-Host "  - $($_.TestName): $($_.Error)" -ForegroundColor Red
    }
}

Write-Host ""
if ($failedTests -eq 0) {
    Write-Host "🎉 All tests passed! Your WisdomWealth system is working perfectly!" -ForegroundColor Green
} else {
    Write-Host "⚠️  Some tests failed. Please check the agent implementations and try again." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🌐 Frontend Test Instructions:" -ForegroundColor Cyan
Write-Host "1. Open http://localhost:3000 in your browser" -ForegroundColor White
Write-Host "2. Click Chat to test the interactive interface" -ForegroundColor White
Write-Host "3. Try the test messages above in the chat" -ForegroundColor White
Write-Host "4. Verify risk levels and agent responses" -ForegroundColor White