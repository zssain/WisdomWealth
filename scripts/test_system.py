# Test the system locally before deployment

import requests
import json
from datetime import datetime

# Test data
BASE_URL = "http://localhost:8000"  # Change to your Railway URL for remote testing
test_scenarios = [
    {
        "name": "SSN Scam",
        "input": "Someone called saying they're from the IRS and need my Social Security number to avoid arrest",
        "expected_risk": "HIGH",
        "expected_agents": ["fraud", "family"]
    },
    {
        "name": "Gift Card Scam", 
        "input": "A caller said I owe money and must pay with gift cards immediately",
        "expected_risk": "HIGH",
        "expected_agents": ["fraud"]
    },
    {
        "name": "Medical Bill",
        "input": "I received a $2000 hospital bill that seems too high",
        "expected_risk": "MEDIUM",
        "expected_agents": ["healthcare"]
    },
    {
        "name": "Family Emergency",
        "input": "Someone called saying my grandson is in jail and needs $5000 bail money right now", 
        "expected_risk": "HIGH",
        "expected_agents": ["fraud", "family"]
    },
    {
        "name": "Estate Planning",
        "input": "I need help updating my will and power of attorney documents",
        "expected_risk": "LOW",
        "expected_agents": ["estate"]
    },
    {
        "name": "Tech Support",
        "input": "Microsoft called about a virus on my computer and wants remote access",
        "expected_risk": "HIGH", 
        "expected_agents": ["fraud"]
    }
]

def test_health():
    """Test health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        print(f"✅ Health check: {response.status_code}")
        if response.status_code == 200:
            health_data = response.json()
            print(f"   Agents: {health_data.get('agents', {})}")
            print(f"   Database: {health_data.get('database', {})}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_scenario(scenario):
    """Test individual scenario"""
    try:
        payload = {
            "user_id": f"test_user_{datetime.now().strftime('%H%M%S')}",
            "text": scenario["input"],
            "meta": {"test": True}
        }
        
        response = requests.post(
            f"{BASE_URL}/route", 
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code != 200:
            print(f"❌ {scenario['name']}: HTTP {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
            return False
            
        data = response.json()
        
        # Check response structure
        required_fields = ["response", "risk", "agent_traces", "actions"]
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            print(f"❌ {scenario['name']}: Missing fields {missing_fields}")
            return False
        
        # Check risk level
        actual_risk = data["risk"].upper()
        expected_risk = scenario["expected_risk"]
        risk_match = actual_risk == expected_risk
        
        # Check agents activated
        actual_agents = data["agent_traces"]
        expected_agents = scenario["expected_agents"] 
        agents_match = any(agent in actual_agents for agent in expected_agents)
        
        # Overall pass/fail
        passed = risk_match and agents_match
        status = "✅" if passed else "⚠️"
        
        print(f"{status} {scenario['name']}")
        print(f"   Input: {scenario['input'][:60]}...")
        print(f"   Risk: {actual_risk} (expected: {expected_risk}) {'✓' if risk_match else '✗'}")
        print(f"   Agents: {actual_agents} (expected: {expected_agents}) {'✓' if agents_match else '✗'}")
        print(f"   Response: {data['response'][:80]}...")
        print(f"   Actions: {data.get('actions', [])}")
        print()
        
        return passed
        
    except Exception as e:
        print(f"❌ {scenario['name']}: Exception {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 WisdomWealth System Testing")
    print("=" * 50)
    
    # Test health first
    if not test_health():
        print("❌ System health check failed. Please fix before continuing.")
        return
    
    print()
    print("🔍 Testing Scenarios...")
    print("-" * 30)
    
    # Test all scenarios
    results = []
    for scenario in test_scenarios:
        result = test_scenario(scenario)
        results.append((scenario["name"], result))
    
    # Summary
    print("📊 Test Results Summary")
    print("-" * 25)
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {name}")
    
    print(f"\nOverall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 All tests passed! System is ready for deployment.")
    else:
        print("⚠️ Some tests failed. Please review and fix issues.")

if __name__ == "__main__":
    main()